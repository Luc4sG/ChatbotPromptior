import os
import re
import bs4
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings
#TODO: revisar si son los imports correctos
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader


class DataStore:
    def __init__(self):
        """Inicializa la base de datos vectorial y carga los datos si es necesario."""
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
        self.vectorstore = Chroma(
            collection_name=settings.collection_name,
            embedding_function=self.embeddings,
            persist_directory=settings.chroma_db_dir
        )
        
        # Verificar si ya hay documentos en la base, si no, cargar los documentos
        data = self.query_all()
        if not data["ids"]:  
            self.load_documents()

    def load_documents(self):
        """Carga documentos y sitios web en la base vectorial si aún no están almacenados."""
        web_documents = self.ingest_url()
        pdf_documents = self.ingest_pdf(settings.pdf_path)

        all_documents = web_documents + pdf_documents
        print(all_documents)
        if all_documents:  
            self.vectorstore.add_documents(all_documents)

    def clean_text(self, text: str) -> str:
        text = text.replace("\n", " ")  
        text = re.sub(r'\s+', ' ', text).strip()  

        return text


    def ingest_pdf(self, pdf_path: str) -> List[Document]:      
        if not os.path.exists(pdf_path):
            #TODO: transalate to english
            print(f"el archivo pdf {pdf_path} no existe")
            return []

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        loader = PyPDFLoader(file_path=pdf_path)
        documents = loader.load_and_split(text_splitter=text_splitter)


        for doc in documents:
            doc.page_content = self.clean_text(doc.page_content)

        return documents

    def ingest_url(self) -> List[Document]:      
        if not settings.urls:
                        #TODO: transalate to english
            print("no hay urls configuradas para la ingesta")
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


# Instancia única de la base de datos vectorial
vectorstore = DataStore()
print(vectorstore.query_all())