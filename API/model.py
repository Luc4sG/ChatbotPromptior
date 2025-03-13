#modulo de Modelo LLM va a contener el promt pre establecido, limitaciones, lenguaje y la defincion propia del modelo llm de openai
import os
from data_store import vectorstore 
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

class Model:
    def __init__(self):
        #definir el modelo
        self.model = ChatOpenAI(
            api_key=os.environ['OPENAI_API_KEY'],
            model="gpt-3.5-turbo",
        )
        self.vectorstore = vectorstore.get_vectorstore()
        #se selecciona el retriever de tipo mmr para una busqueda variada que incluya tanto el pdf como la pagina de Promptior
        #self.retriever = self.vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10, "lambda_mult": 0.5})
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are an AI assistant that answers questions based on the provided context. "
                "Your answers should be concise unless the user explicitly requests otherwise. "
                "If you don’t know the answer, respond with: 'I can't answer that question'. "
                "Provide the answer in the language requested by the user: {language}.\n"
                "---\n"
                "Context: {context}"
            ),
            HumanMessagePromptTemplate.from_template("{question}")
        ])

        self.output_parser = StrOutputParser()

    def get_query(self, question: str, language: str):

        docs = self.retriever.invoke(question)
        context = " ".join([doc.page_content  for doc in docs])
        message = self.prompt.format_messages(
            question=question,
            language=language,
            context=context
        )

        return self.model.invoke(message)

#instacia global
model = Model()
