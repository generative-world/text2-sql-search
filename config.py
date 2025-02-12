
import os

POSTGRES_CONNECTION_STRING = os.environ.get("POSTGRES_CONNECTION_STRING") or "postgresql://postgres:password@postgres:5432/your_db"  # Replace with your PostgreSQL connection details
WEAVIATE_URL = os.environ.get("WEAVIATE_URL") or "http://weaviate:8080"
ARANGODB_URL = os.environ.get("ARANGODB_URL") or "http://arangodb:8529"
ARANGODB_DATABASE = os.environ.get("ARANGODB_DATABASE") or "my_arangodb"
ARANGODB_USER = os.environ.get("ARANGODB_USER") or "root"
ARANGODB_PASSWORD = os.environ.get("ARANGODB_PASSWORD") or "password"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
