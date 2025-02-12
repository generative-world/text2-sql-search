
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt.
RUN pip install -r requirements.txt

COPY..

# Set environment variables (or use a.env file and docker-compose)
ENV POSTGRES_CONNECTION_STRING "postgresql://postgres:password@postgres:5432/your_db"
ENV WEAVIATE_URL "http://weaviate:8080"
ENV ARANGODB_URL "http://arangodb:8529"
ENV ARANGODB_DATABASE "my_arangodb"
ENV ARANGODB_USER "root"
ENV ARANGODB_PASSWORD "password"
ENV GEMINI_API_KEY "YOUR_ACTUAL_API_KEY"  # Consider using Docker secrets

CMD ["python", "api.py"]
