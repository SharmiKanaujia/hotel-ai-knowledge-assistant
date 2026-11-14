
import json
from pathlib import Path
from rag.llm import generate_answer
from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel, StringConstraints

app = FastAPI(title="Hotel AI Knowledge Assistant")

class QuestionRequest(BaseModel):
    question: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=500
        )
    ]
# Load our fictional hotel knowledge
faq_path = Path(__file__).with_name("hotel_faq.json")

with faq_path.open("r", encoding="utf-8") as file:
    hotel_faq = json.load(file)


@app.get("/")
def home():
    return {"message": "Welcome to Hotel AI Assistant!"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.lower()

    for faq in hotel_faq:
        for keyword in faq["keywords"]:
            if keyword in question:
                return {
                    "question": request.question,
                    "answer": faq["answer"],
                    "source": faq["id"]
                }

    return {
        "question": request.question,
        "answer": "I could not find that information.",
        "source": None
    }
@app.post("/ask/rag")
def ask_rag_question(request: QuestionRequest):
    return generate_answer(request.question)