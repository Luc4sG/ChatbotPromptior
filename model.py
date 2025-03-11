#modulo de Modelo LLM va a contener el promt pre establecido, limitaciones, lenguaje y la defincion propia del modelo llm de openai
import os
from data_store import vectorstore 
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class Model:
    def __init__(self):
        #definir el modelo
        self.model = ChatOpenAI(
            api_key=os.environ['OPENAI_API_KEY'],
            model="gpt-3.5-turbo",
        )
        self.vectorstore = vectorstore
        self.retriever = self.vectorstore.as_retriever()
        self.prompt = """
        Answer the question based only on the following context: {context}
        ---
        Question: {question}
        """

        ##revisar la sintaxis de la cadena
        self.rag_chain = (
            {"context": self.retriever | RunnablePassthrough(),
             "question": RunnablePassthrough(),}
            | ChatPromptTemplate.from_template(self.prompt)
            | self.model
            | StrOutputParser()
        )
