# config.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List

load_dotenv()  

class Settings(BaseSettings):
    openai_api_key: str = os.environ.get("OPENAI_API_KEY")
    chroma_db_dir: str = os.environ.get("CHROMA_DB_DIR", "./db_chroma")
    collection_name: str = os.environ.get("COLLECTION_NAME", "promptior")
    environment: str = os.environ.get("ENVIRONMENT", "dev")
    pdf_path: str = "./public/AI Engineer.pdf"
    urls: List[str] = [
        "https://www.promtior.ai/",
        "https://www.promtior.ai/service"
    ]
    
settings = Settings()