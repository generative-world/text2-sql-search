
import psycopg2
import weaviate
from arango import ArangoClient
from arango.exceptions import DocumentNotFoundError
from config import POSTGRES_CONNECTION_STRING, WEAVIATE_URL, ARANGODB_URL, ARANGODB_DATABASE, ARANGODB_USER, ARANGODB_PASSWORD

def connect_postgres():
    try:
        return psycopg2.connect(POSTGRES_CONNECTION_STRING)
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def connect_weaviate():
    try:
        return weaviate.Client(WEAVIATE_URL)
    except Exception as e:
        print(f"Error connecting to Weaviate: {e}")
        return None

def connect_arangodb():
    try:
        client = ArangoClient(hosts=ARANGODB_URL)
        return client.db(ARANGODB_DATABASE, username=ARANGODB_USER, password=ARANGODB_PASSWORD)
    except Exception as e:
        print(f"Error connecting to ArangoDB: {e}")
        return None

def execute_postgres_query(conn, sql_query):
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")
        return None

def create_weaviate_schema(client, employee_class):
    if not client:
        return
    client.schema.delete_all()
    client.schema.add(employee_class)

def create_weaviate_object(client, data_object, vector):
    if not client:
        return
    client.data_object.create(data_object, "Employee", vector=vector)

def search_weaviate(client, near_text):
    if not client:
        return None
    return client.query.get("Employee", ["employee_id", "name", "department", "salary", "arangodb_key"]).with_near_text(near_text).do()

def insert_arangodb_document(db, document, collection_name="employees"):
    if not db:
        return None
    try:
        return db.collection(collection_name).insert(document)
    except Exception as e:
        print(f"ArangoDB Insert Error: {e}")
        return None

def execute_arangodb_query(db, query):
    if not db:
        return None
    try:
        return list(db.aql.execute(query))
    except Exception as e:
        print(f"ArangoDB Query Error: {e}")
        return None

def get_arangodb_document(db, key, collection_name="employees"):
    if not db:
        return None
    try:
        return db.collection(collection_name).get(key)
    except DocumentNotFoundError:
        return None
    except Exception as e:
        print(f"ArangoDB Get Error: {e}")
        return None
