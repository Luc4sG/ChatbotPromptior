#modulo de Modelo LLM va a contener el promt pre establecido, limitaciones, lenguaje y la defincion propia del modelo llm de openai
import os
from langchain_openai import ChatOpenAI

class Model:
    def __init__(self):
        #definir el modelo
        model = ChatOpenAI(
            api_key=os.environ['OPENAI_API_KEY'],
            model="gpt-3.5-turbo",
        )


    