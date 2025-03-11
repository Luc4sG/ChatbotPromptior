import os
import bs4
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader

#mi data store deberia ser una instancia de mi base de datos vectoriales, ademas de inicializarse por unica vez cargando los datos en la base;
class DataStore:
    def __init__(self) -> Chroma:
        #instanciar la base de datos vectorial
        self.openai_api_key = settings.openai_api_key
        self.collection_name = settings.collection_name
        self.chroma_db_dir = settings.chroma_db_dir
        self.url_list = settings.urls
        self.pdf_file = settings.pdf_path
        
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.chroma_db_dir
        )
        data = self.vectorstore.get()
        if data["ids"] is None:
            self.load_documents(self) 
        
        return vectorstore;

    def load_documents(self):
        """
        load the documents and websites into the vectorstore
        revisar para agregar ids a cada documento para hacer la ingesta una sola vez y no duplicar los datos
        """
        for url in self.url_list:
            documents = self.ingest_url(url)
            self.vectorstore.add_documents(documents)
        
        documents = self.ingest_pdf(self.pdf_file)
        self.vectorstore.add_documents(documents)
    
    def ingest_pdf(self,  pdf_path: str) -> List[Document]:
        """
        ingest the pdf file into the vectorstore
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        loader = PyPDFLoader(
            file_path=pdf_path,
        )

        documents = loader.load_and_split(text_splitter=text_splitter)  
        return documents;



    def ingest_url(self, url : str)-> List[Document]:
        """
        ingest the urls into the vectorstore
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        loader = WebBaseLoader(
            web_path=url,
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    class_ = ("SITE_HEADER", "PAGES_CONTAINER", "SITE_FOOTER")
                )),
        )

        documents = loader.load_and_split(text_splitter=text_splitter)
        return documents;

#buscar la forma correcta de instanciar la vectorstore 
vectorstore = DataStore().__init__();