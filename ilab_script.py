import sys
import psycopg2
import pandas as pd
from getpass import getpass

def run_query(query):

    print("function started")
    user = input("Enter your Rutgers NetID: ")
    password = getpass("Enter your Rutgers password: ")

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
        print(df)

        cur.close()
        conn.close()

    except Exception as e:
        print("ERROR OCCURRED")
        print("Error:", e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ilab_script.py \"SELECT ...\"")
    else:
        query = sys.argv[1]
        run_query(query)