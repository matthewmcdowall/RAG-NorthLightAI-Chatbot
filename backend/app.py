from fastapi import FastAPI, Query
from backend.retrieval import get_answer

app = FastAPI(title="NorthLightAI Chatbot")

@app.get("/")
def root():
    return {"message": "NorthLightAI Chatbot API"}

@app.get("/chat")
def chat(query: str = Query(..., description="User question")):
    answer = get_answer(query)
    return {"answer": answer}
