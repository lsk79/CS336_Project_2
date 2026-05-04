import re
import shlex
from dataclasses import dataclass
import getpass
import paramiko


##Lucas --> (Config)

ILAB_HOST = "python.cs.rutgers.edu"
REMOTE_PYTHON = "python3"
REMOTE_SCRIPT_PATH = "~/ilab_script.py"

##Shreya--> 

def run_llm(question):
    q = question.lower()

    if "average income" in q:
        return "SELECT AVG(applicant_income_000s) FROM application;"
    elif "loan value greater than" in q or "loan amount greater than" in q:
        return "SELECT COUNT(*) FROM application WHERE loan_amount_000s > applicant_income_000s;"
    elif "common loan denial" in q or "most common denial" in q:
        return """SELECT d.denial_reason_name_1, COUNT(*)
FROM application a
JOIN denialreason1 d ON a.denial_reason_1 = d.denial_reason_1
GROUP BY d.denial_reason_name_1
ORDER BY COUNT(*) DESC
LIMIT 1;"""
    else:
        return "SELECT * FROM application LIMIT 5;"
##Angela -->

def extract_query(llm_response: str) -> str:
    match = re.search(r"'''sql\s*(.*?)\s*'''", llm_response, re.DOTALL | re.IGNORECASE)
    if not match:
        match = re.search(r"'''\s*(.*?)\s*'''", llm_response, re.DOTALL)
    if match: 
        query = match.group(1).strip()
    else:
        raw_match = re.search(r"(SELECT\s+.*?;)", llm_response, re.DOTALL | re.IGNORECASE)
        query = raw_match.group(1).strip() if raw_match else "ERROR: There are no SELECT query found."
    if "ERROR" not in query:
        query = query.replace('\n', ' ').replace('\r', ' ')
        query = " ".join(query.split())
    return query


##Lucas --> (SELECT query check)
def validate_select_query(sql_query: str) -> tuple[bool, str]:
    if sql_query.startswith("ERROR:"):
        return False, sql_query

    normalized = sql_query.strip().upper()

    if not (normalized.startswith("SELECT") or normalized.startswith("WITH")):
        return False, "Only SELECT/WITH read-only queries are allowed."

    forbidden_words = [
        "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE",
        "GRANT", "REVOKE", "MERGE", "CALL", "EXEC", "COPY"
    ]

    for word in forbidden_words:
        if re.search(rf"\b{word}\b", normalized):
            return False, f"Unsafe SQL rejected because it contains: {word}"

    if normalized.count(";") > 1:
        return False, "Only one SQL statement is allowed."

    return True, "OK"


##Lucas --> (ssh integration)


@dataclass
class RemoteResult:
    exit_code: int
    output: str
    errors: str


def build_remote_command(sql_query: str, db_user: str) -> str:

    return (
        f"{shlex.quote(REMOTE_PYTHON)} "
        f"{shlex.quote(REMOTE_SCRIPT_PATH)} "
        f"--db-user {shlex.quote(db_user)} "
        f"{shlex.quote(sql_query)}"
    )


def run_query_on_ilab(
    sql_query: str,
    ssh_user: str,
    ssh_password: str,
    db_user: str,
    db_password: str,) -> RemoteResult:

    command = build_remote_command(sql_query, db_user)

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=ILAB_HOST,
            username=ssh_user,
            password=ssh_password,
            look_for_keys=False,
            allow_agent=False,
            timeout=20,
        )

        stdin, stdout, stderr = client.exec_command(command)

        # Send database/PostgreSQL password through encrypted SSH stdin.
        stdin.write(db_password + "\n")
        stdin.flush()
        stdin.channel.shutdown_write()

        output = stdout.read().decode("utf-8", errors="replace")
        errors = stderr.read().decode("utf-8", errors="replace")
        exit_code = stdout.channel.recv_exit_status()

        return RemoteResult(exit_code=exit_code, output=output, errors=errors)

    finally:
        client.close()

## Lucas --> (Main interactive prog)

def main() -> None:

    print("Natural Language to SQL over iLab SSH")
    print("Type exit to quit.\n")

    ssh_user = input("Enter your Rutgers NetID / iLab username: ").strip()
    ssh_password = getpass.getpass("Enter your Rutgers/iLab password: ")

    db_user_input = input(f"Enter PostgreSQL username/database [{ssh_user}]: ").strip()
    db_user = db_user_input if db_user_input else ssh_user

    use_same = input("Use the same password for PostgreSQL? [Y/n]: ").strip().lower()
    if use_same in ("", "y", "yes"):
        db_password = ssh_password
    else:
        db_password = getpass.getpass("Enter PostgreSQL password: ")

    while True:
        user_question = input("\nEnter question (or type exit): ").strip()

        if user_question == "exit":
            print("Exiting...")
            break

        if not user_question:
            print("Please enter a question or type exit.")
            continue

        # nts: Shreya's part.
        raw_output = run_llm(user_question)
        print("\n-- LLM Output --")
        print(raw_output)

        # nts: Angela's part.
        processed_sql = extract_query(raw_output)
        print("\n-- Clean SQL --")
        print(processed_sql)

        # nts: Lucas's part 
        is_valid, message = validate_select_query(processed_sql)
        if not is_valid:
            print(f"\nQuery rejected: {message}")
            continue

        print("\nExecuting on iLab server...")
        try:
            result = run_query_on_ilab(
                sql_query=processed_sql,
                ssh_user=ssh_user,
                ssh_password=ssh_password,
                db_user=db_user,
                db_password=db_password,
            )
        except Exception as exc:
            print(f"SSH error: {exc}")
            continue

        print("\n-- Remote Output --")
        print(result.output if result.output else "(No output returned.)")

        if result.errors:
            print("\n-- Remote Error Output --")
            print(result.errors)

        if result.exit_code != 0:
            print(f"\nRemote command exited with code {result.exit_code}.")


if __name__ == "__main__":
    main()
