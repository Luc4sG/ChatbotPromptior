import os
from config import settings
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

#mi data store deberia ser una instancia de mi base de datos vectoriales, ademas de inicializarse por unica vez cargando los datos en la base;
class DataStore:
    def __init__(self):
        #instanciar la base de datos vectorial
        self.openai_api_key = settings.openai_api_key
        self.collection_name = settings.collection_name
        self.chroma_db_dir = settings.chroma_db_dir
        
        # Inicializamos embeddings y la base vectorial
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.chroma_db_dir
        )
    


    def get_vectorstore():
        """
        Get the vector store or create one in case it doesn't exist
        """
        
            