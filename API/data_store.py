import os
import re
import boto3
import json
import bs4
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader


class DataStore:
    def __init__(self):
        """Inicializa la base de datos vectorial y carga los datos si es necesario."""
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.get_openai_api_key())
        self.vectorstore = Chroma(
            collection_name=settings.collection_name,
            embedding_function=self.embeddings,
            persist_directory=settings.chroma_db_dir
        )
        
        # Verificar si ya hay documentos en la base, si no, cargar los documentos
        data = self.query_all()
        if not data["ids"]:  
            self.load_documents()
    
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
    
    def load_documents(self):
        web_documents = self.ingest_url()
        pdf_documents = self.ingest_pdf(settings.pdf_path)

        all_documents = web_documents + pdf_documents
        if all_documents:  
            self.vectorstore.add_documents(all_documents)

    def clean_text(self, text: str) -> str:
        text = text.replace("\n", " ")  
        text = re.sub(r'\s+', ' ', text).strip()  

        return text

    def ingest_pdf(self, pdf_path: str) -> List[Document]: 
        if not os.path.exists(pdf_path):

            print(f"the pdf file path {pdf_path} does not exist")
            return []

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        loader = PyPDFLoader(file_path=pdf_path)
        documents = loader.load_and_split(text_splitter=text_splitter)


        for doc in documents:
            doc.page_content = self.clean_text(doc.page_content)

        return documents

    def ingest_url(self) -> List[Document]:      
        if not settings.urls:

            print("No URLs provided")
            return []

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

        loader = WebBaseLoader(
            web_path=settings.urls,
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(

                    class_=("SITE_HEADER", "PAGES_CONTAINER", "SITE_FOOTER")
                )
            ),
        )

        documents = loader.load_and_split(text_splitter=text_splitter)
        for doc in documents:
            doc.page_content = self.clean_text(doc.page_content)

        return documents

    def query_all(self):
        return self.vectorstore.get()

    def get_vectorstore(self):

        return self.vectorstore


vectorstore = DataStore()

