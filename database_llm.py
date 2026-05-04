import re
import subprocess

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
while True:
    question = input("Enter question (or type exit): ")

    if question == "exit":
        break

    print("\n--- LLM OUTPUT ---")
    print(run_llm(question))
    print()

##Angela -->

def extract_query(llm_response: str) -> str:
    match = re.search(r"'''sql\s*(.*?)\s*'''", llm_response, re.DOTALL | re.IGNORECASE)
    if not match:
        match = re.search(r"'''\s*(.*?)\s*'''", llm_response, re.DOTALL)
    if match: 
        query = match.group(1).strip()
    else:
        raw_match = re.search(r"(SELECT\s+.*?;)", llm_response, re.DOTALL | re.IGNORECASE)
        query = match.group(1).strip() if match else "ERROR: There are no SELECT query found."
    if "ERROR" not in query:
        query = query.replace('\n', ' ').replace('\r', ' ')
        query = " ".join(query.split())
    return query

if __name__ == "--main--":
    while True:
        user_question = input("\nEnter question (or type exit): ")
        if user_question.lower() == "exit":
            print("Exiting...")
            break
        raw_output = run_llm(user_question)
        print("\n-- RAW LLM OUTPUT --")
        print(raw_output)
        processed_sql = extract_query(raw_output)
        if "ERROR" in processed_sql:
            print(f"\n{processed_sql}")
        else:
            print("\n--CLEAN SQL FOR ILAB --")
            print(processed_sql)
            print("\nExecuting on iLab server...")
            subprocess.run(["python3", "ilab_script.py", processed_sql])

    
    
