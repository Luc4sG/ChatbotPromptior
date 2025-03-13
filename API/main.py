#expose the model with langserve 
from fastapi import FastAPI, requests
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from pydantic import BaseModel
from model import model
from model import QueryInput

app = FastAPI(title="RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class QueryRequest(BaseModel):
    question: str
    language: str


chain = model.chain
add_routes(app,chain.with_types(input_type=QueryInput) ,path="/chat")

@app.get("/")
def root():
    return {"response": "Chatbot RAG funcionando!"}

