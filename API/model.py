#modulo de Modelo LLM va a contener el promt pre establecido, limitaciones, lenguaje y la defincion propia del modelo llm de openai
import os
import boto3
import json
from pydantic import BaseModel
from config import settings
from data_store import vectorstore 
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate



class QueryInput(BaseModel):
    question: str

class Model:
    def __init__(self):
        #definir el modelo
        self.model = ChatOpenAI(
            api_key=self.get_openai_api_key(),
            model="gpt-3.5-turbo",
        )
        self.vectorstore = vectorstore.get_vectorstore()
        #se selecciona el retriever de tipo mmr para una busqueda variada que incluya tanto el pdf como la pagina de Promptior
        # self.retriever = self.vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10, "lambda_mult": 0.5})
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are an AI assistant that answers questions based on the provided context. "
                "Your answers should be concise unless the user explicitly requests otherwise. "
                "If you don’t know the answer, respond with: 'I can't answer that question'. "
                "Provide the answer in the language that the question was asked in. "
                "---\n"
                "Context: {context}"
            ),
            HumanMessagePromptTemplate.from_template("{question}")
        ])

        self.output_parser = StrOutputParser()

        self.chain = ( RunnableLambda(self.validate_input) |
            RunnableMap({
            "context": self.retrieve_context,
            "question": lambda x: x["question"]
        }) | self.prompt | self.model | self.output_parser)

    def get_openai_api_key(self):
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

    def validate_input(self, inputs: dict):
        validated_data = QueryInput(**inputs)  
        return validated_data.model_dump()

    def retrieve_context(self, inputs: dict):

        docs = self.retriever.invoke(inputs["question"])
        context = " ".join([doc.page_content  for doc in docs])
        inputs["context"] = context
        return inputs


#instacia global
model = Model()
