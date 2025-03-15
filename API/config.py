# config.py
import os
import boto3
import json
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List

load_dotenv()  

def get_openai_api_key():
    secret_name = os.getenv("AWS_SECRET_NAME", "chatbot_api_key")
    region_name = os.getenv("AWS_REGION", "us-east-1")
    try:
        client = boto3.client("secretsmanager", region_name=region_name)
        
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])
        return secret["OPENAI_API_KEY"]
    except Exception as e:
        print(f"Error al obtener secreto: {e}")
        return os.getenv("OPENAI_API_KEY", "default_key_if_missing")

class Settings(BaseSettings):
    openai_api_key: str = get_openai_api_key()
    chroma_db_dir: str = os.environ.get("CHROMA_DB_DIR", "db_chroma")
    collection_name: str = os.environ.get("COLLECTION_NAME", "promptior")
    environment: str = os.environ.get("ENVIRONMENT", "dev")
    pdf_path: str = "./public/AI Engineer.pdf"
    urls: List[str] = [
        "https://www.promtior.ai/",
        "https://www.promtior.ai/service"
    ]

settings = Settings()