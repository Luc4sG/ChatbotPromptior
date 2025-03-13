#expose the model with langserve 
from fastapi import FastAPI, requests
from pydantic import BaseModel
from model import model
import uvicorn

app = FastAPI(title="RAG Chatbot")

class QueryRequest(BaseModel):
    question: str
    language: str


@app.post("/query")
def query_endpoint(req: QueryRequest):
    answer = model.get_query(req.question, req.language)
    return {"response": answer}

@app.get("/")
def root():
    return {"response": "Chatbot RAG funcionando!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)