def make_prompt(schema, question):
    return f"""
Write a PostgreSQL SELECT query.

Only return SQL. No explanation.

Schema:
{schema}

Question:
{question}

SQL:
"""

def main():
    with open("schema_prompt.sql", "r") as f:
        schema = f.read()

    while True:
        question = input("Enter question (or type exit): ")

        if question == "exit":
            break

        prompt = make_prompt(schema, question)

        print("\n--- PROMPT ---")
        print(prompt)
        print("\n--- LLM OUTPUT WILL GO HERE ---\n")

if __name__ == "__main__":
    main()
