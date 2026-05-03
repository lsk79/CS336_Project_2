# CS336_Project_2

## Team Contributions - Lucas Bandeira, Shreya Bhatlapenumarti, Angela Ding, Lakshmi Kottapalli

### Lakshmi K. --> Created python program to take in SQL query and print out results on the database. Used psycopg2 for PostgreSQL connection and getpass for passwords. 
### Shreya B. --> Implemented the LLM prompt and query generation logic. Created database_llm.py, which takes natural language user questions and converts them into SQL SELECT queries based on the Project 1 schema. Also built a loop to accept user input and tested the program on sample queries such as average income and loan comparisons.
### Angela D. --> Created the schema_subset file which maps the normalized relations from Project 1 which includes the Normalized App, Agency, and ActionTaken tables. Also, I am responsible for text processing and extraction so I added the extract_query function in database_llm file which isolate the SELECT statements and make sure the output is cleaned and concise so it can be safely executed.  
### Lucas B. -->
