from flask import Flask, request, jsonify
from config import POSTGRES_CONNECTION_STRING
from db_services import connect_postgres, execute_postgres_query, create_weaviate_object, search_weaviate, insert_arangodb_document, execute_arangodb_query, create_weaviate_schema
from gemini_services import connect_gemini, generate_sql, generate_embedding

app = Flask(__name__)

# Initialize database connections and the Gemini client
conn_pg = connect_postgres()
client_weaviate = connect_weaviate()
db_arangodb = connect_arangodb()
gemini_client = connect_gemini()

# Check if all connections were successfully established
if not all([conn_pg, client_weaviate, db_arangodb, gemini_client]):
    print("Failed to establish one or more connections. Exiting.")
    exit()  # Exit the application if any connection failed

# Define the schema for the Employee class in Weaviate
employee_class = {
    "class": "Employee",
    "properties": [
        {"name": "employee_id", "dataType": ["int"]},
        {"name": "name", "dataType": ["text"]},
        {"name": "department", "dataType": ["text"]},
        {"name": "salary", "dataType": ["number"]},
        {"name": "arangodb_key", "dataType": ["text"]},
    ],
}
create_weaviate_schema(client_weaviate, employee_class)

# API endpoint to generate SQL query from natural language
@app.route('/api/sql', methods=['POST'])
def get_sql_query():
    try:
        data = request.get_json()
        question = data.get('question')
        table_schema = data.get('table_schema')

        if not question or not table_schema:
            return jsonify({'error': 'Missing question or table_schema'}), 400

        sql_query = generate_sql(gemini_client, question, table_schema)
        if sql_query:
            return jsonify({'sql_query': sql_query}), 200
        else:
            return jsonify({'error': 'Could not generate SQL query'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to execute a SQL query
@app.route('/api/execute_sql', methods=['POST'])
def execute_sql():
    try:
        data = request.get_json()
        sql_query = data.get('sql_query')
        if not sql_query:
            return jsonify({'error': 'Missing sql_query'}), 400

        results = execute_postgres_query(conn_pg, sql_query)
        if results is not None:
            return jsonify({'results': results}), 200
        else:
            return jsonify({'error': 'Error executing SQL query'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint for semantic search
@app.route('/api/semantic_search', methods=['POST'])
def semantic_search():
    try:
        data = request.get_json()
        query = data.get('query')
        if not query:
            return jsonify({'error': 'Missing query'}), 400

        embedding = generate_embedding(gemini_client, query)
        if embedding is None:
            return jsonify({'error': 'Error generating embedding'}), 500

        near_text = {"concepts": [query]}
        result_weaviate = search_weaviate(client_weaviate, near_text)

        if result_weaviate and "data" in result_weaviate and "Get" in result_weaviate["data"] and "Employee" in result_weaviate["data"]["Get"]:
            results =
            for employee in result_weaviate["data"]["Get"]["Employee"]:
                employee_id = employee["employee_id"]
                arangodb_key = employee["arangodb_key"]
                name = employee["name"]
                department = employee["department"]
                salary = employee["salary"]

                cursor_pg = conn_pg.cursor()
                cursor_pg.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
                full_employee_data = cursor_pg.fetchone()

                related_employees =
                try:
                    arangodb_result = execute_arangodb_query(db_arangodb, f"""
                    FOR d IN departments
                      FILTER d.name == '{department}'
                      FOR e IN employees
                        FILTER e.department_id == d.id
                        RETURN e
                    """)
                    related_employees = list(arangodb_result)
                except Exception as e:
                    print(f"ArangoDB Query Error: {e}")

                results.append({
                    "employee_id": employee_id,
                    "name": name,
                    "department": department,
                    "salary": salary,
                    "full_employee_data": full_employee_data,
                    "related_employees": related_employees
                })
            return jsonify({'results': results}), 200
        else:
            return jsonify({'results':}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.teardown_appcontext
def close_connections(exception):
    if conn_pg is not None:
        conn_pg.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
