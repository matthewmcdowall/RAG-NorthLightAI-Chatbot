from fastapi import FastAPI, Query
from retrieval import get_answer

app = FastAPI()

@app.get("/chat")
def chat(query: str = Query(..., description="User question")):
    answer = get_answer(query)
    return {"answer": answer}
