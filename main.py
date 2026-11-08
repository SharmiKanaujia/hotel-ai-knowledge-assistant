
import json
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Hotel AI Knowledge Assistant")

class QuestionRequest(BaseModel):
    question: str

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
