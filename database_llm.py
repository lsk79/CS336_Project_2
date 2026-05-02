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
