
from google.generativeai import GeminiClient
from config import GEMINI_API_KEY

def connect_gemini():
    try:
        return GeminiClient(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error connecting to Gemini: {e}")
        return None

def generate_sql(gemini_client, question, table_schema, prompt_file="prompts/generate_sql.txt"):
    if not gemini_client:
        return None
    try:
        with open(prompt_file, "r") as f:
            prompt_template = f.read()
        prompt = prompt_template.format(table_schema=table_schema, question=question)
        response = gemini_client.generate_text(prompt)
        return response.result.strip()
    except Exception as e:
        print(f"Gemini SQL Generation Error: {e}")
        return None

def generate_embedding(gemini_client, text, prompt_file="prompts/generate_embedding.txt"):
    if not gemini_client:
        return None
    try:
        with open(prompt_file, "r") as f:
            prompt_template = f.read()
        prompt = prompt_template.format(text=text)
        response = gemini_client.generate_text(prompt)
        return response.result
    except Exception as e:
        print(f"Gemini Embedding Generation Error: {e}")
        return None
