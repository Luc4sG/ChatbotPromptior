# config.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List

load_dotenv()  

class Settings(BaseSettings):
    def get_openai_api_key():
        secret_path = "/run/secrets/openai_api_key"
        if os.path.exists(secret_path):
            with open(secret_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return os.getenv("OPENAI_API_KEY", "default_key_if_missing")
    
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