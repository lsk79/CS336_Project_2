import sys
import argparse
import re
import psycopg2
import pandas as pd
from getpass import getpass

##Lucas --> (Safety valid. for SSH )

def validate_select_query(query: str) -> tuple[bool, str]:

    normalized = query.strip().upper()

    if not (normalized.startswith("SELECT") or normalized.startswith("WITH")):
        return False, "Only SELECT/WITH queries are allowed."

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


## Lakshmi --> (Query exec)

def read_password() -> str:

    if sys.stdin.isatty():
        return getpass("Enter your Rutgers/PostgreSQL password: ")
    
    password = sys.stdin.readline().rstrip('\n')
    
    if not password:
        raise ValueError("No db password received.")
    return password

def run_query(query: str, user: str) -> int:

    ## Added some validation changes (Lucas)
    is_valid, message = validate_select_query(query)
    if not is_valid:
        print("Error:", message)
        return 2

    password = read_password()

    # make sure terminal shows (myenv) before running because ilab does not allow global pip install
    # Use this to get in the right environment with everything needed installed
        # python3 -m venv myenv
        # source myenv/bin/activate
        # pip install pandas psycopg2-binary
    # run the file using ' python3 ilab_script.py "SELECT * FROM "name of db" LIMIT 5;" '
    # use only SELECT queries and use quotations for query

    try:
        conn = psycopg2.connect(
            host="postgres.cs.rutgers.edu",
            database=user,
            user=user,
            password=password
        )
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {user};")
        cur.execute(query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        df = pd.DataFrame(rows, columns=colnames)
        if df.empty:
            print("Query executed successfully, but returned no results.")
        else:
            print(df.to_string(index=False))
            
        cur.close()
        conn.close()

        # df = pd.DataFrame(rows, columns=colnames)
        # if df.empty:
        #     print("Query executed successfully, but returned no results.")
        # else:
        #     print(df.to_string(index=False))

    except Exception as e:
        print("Error:", e)
        return 1
    return 0


## Lucas --> (Cmd-line arg for SSH call)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a SQL query on iLab PostgreSQL via SSH.")
    
    parser.add_argument(
        "query", 
        help="The SQL SELECT query to execute (enclose in quotes).")
    
    parser.add_argument(
        "--db-user", 
        help="Rutgers NetID / PostgreSQL database username")
    
    return parser.parse_args()

def main() -> int:
    args = parse_args()

    db_user = args.db_user

    if not db_user:
        db_user = input("Enter your Rutgers NetID/PostgreSQL username: ").strip()

    return run_query(args.query, db_user)

if __name__ == "__main__":
    sys.exit(main())