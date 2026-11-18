import os
import json
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, StringConstraints

from rag.llm import generate_answer

app = FastAPI(title="Hotel AI Knowledge Assistant")

@app.get("/chat")
def chat_page():
    chat_file = Path(__file__).resolve().parent / "static" / "chat.html"
    return FileResponse(chat_file)


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


@app.get("/chat/config")
def chat_config():
    enabled = (
        os.getenv("ENABLE_LIVE_RAG", "false").lower()
        == "true"
    )

    return {
        "live_rag_enabled": enabled
    }


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

    # Real AI is disabled unless explicitly enabled
    if os.getenv("ENABLE_LIVE_RAG", "false").lower() != "true":
        raise HTTPException(
            status_code=503,
            detail="Live AI mode is disabled."
        )

    return generate_answer(request.question)



@app.post("/ask/rag/demo")
def ask_rag_demo(request: QuestionRequest):
    question = request.question.lower()

    # Simulate a retrieved hotel document
    if "park" in question or "car" in question:
        return {
            "question": request.question,
            "answer": "Parking is available.",
            "sources": ["parking.md"]
        }

    # Simulate an unknown answer
    return {
        "question": request.question,
        "answer": "I could not find that information.",
        "sources": []
    }
