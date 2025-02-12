from config import POSTGRES_CONNECTION_STRING
from db_services import connect_postgres, execute_postgres_query, create_weaviate_schema, create_weaviate_object, search_weaviate, insert_arangodb_document, execute_arangodb_query
from gemini_services import connect_gemini, generate_sql, generate_embedding

# 1. Connect to Databases and Gemini
conn_pg = connect_postgres()
client_weaviate = connect_weaviate()
db_arangodb = connect_arangodb()
gemini_client = connect_gemini()

if not all([conn_pg, client_weaviate, db_arangodb, gemini_client]):
    print("Failed to establish one or more connections in main.py. Exiting.")
    exit()

try:
    # 2. Example Usage (Your other tasks/scripts go here)

    # Example: Get all employees from PostgreSQL
    sql_query = "SELECT * FROM employees"
    employees_pg = execute_postgres_query(conn_pg, sql_query)
    if employees_pg:
        print("Employees from PostgreSQL (main.py):")
        for employee in employees_pg:
            print(employee)

    # Example: Find employees related to "marketing" (semantic search)
    near_text = {"concepts": ["marketing"]}
    employees_weaviate = search_weaviate(client_weaviate, near_text)

    if employees_weaviate and employees_weaviate["data"] and employees_weaviate["data"]["Get"] and employees_weaviate["data"]["Get"]["Employee"]:
        print("\nEmployees from Weaviate (main.py):")
        for employee in employees_weaviate["data"]["Get"]["Employee"]:
            print(employee)

    # Example: Find employees who work in the 'Sales' department (ArangoDB)
    try:
        sales_employees = execute_arangodb_query(db_arangodb, """
            FOR d IN departments
              FILTER d.name == 'Sales'
              FOR e IN employees
                FILTER e.department_id == d.id
                RETURN e
        """)
        if sales_employees:
            print("\nEmployees in 'Sales' department (ArangoDB):")
            for employee in sales_employees:
                print(employee)
    except Exception as e:
        print(f"Error querying ArangoDB: {e}")


    # Example: Generate embedding for a text
    text_to_embed = "This is a test embedding."
    embedding = generate_embedding(gemini_client, text_to_embed)
    if embedding:
        print(f"\nEmbedding for '{text_to_embed}':")
        print(embedding)  # Print the embedding (be mindful of length)

    # Example: Generate SQL query from natural language
    table_schema = """
        CREATE TABLE employees (
            id SERIAL PRIMARY KEY,
            name TEXT,
            department_id INTEGER REFERENCES departments(id),
            salary REAL
        );
        CREATE TABLE departments (
            id SERIAL PRIMARY KEY,
            name TEXT
        );
    """
    nl_question = "What is the average salary of employees in the Marketing department?"
    sql_query = generate_sql(gemini_client, nl_question, table_schema)
    if sql_query:
        print(f"\nGenerated SQL Query: {sql_query}")

except Exception as e:
    print(f"Error in main.py: {e}")

finally:
    # 3. Close Connections (Important!)
    if conn_pg:
        conn_pg.close()
    if client_weaviate:
        client_weaviate.close() # Close Weaviate client if it exists
    if db_arangodb:
        db_arangodb.close() # Close ArangoDB connection if it exists
