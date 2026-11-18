from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_rag_endpoint(monkeypatch):

    def fake_generate_answer(question):
        return {
            "question": question,
            "answer": "Parking is available.",
            "sources": ["parking.md"]
        }

    monkeypatch.setattr(
        "main.generate_answer",
        fake_generate_answer
    )

    monkeypatch.setenv("ENABLE_LIVE_RAG", "true")

    response = client.post(
        "/ask/rag",
        json={"question": "Where can I leave my car?"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Parking is available."
    assert "parking.md" in response.json()["sources"]


def test_rag_rejects_empty_question():
    response = client.post(
        "/ask/rag",
        json={"question": ""}
    )

    assert response.status_code == 422


def test_rag_disabled_by_default(monkeypatch):
    # Make sure live AI is not enabled
    monkeypatch.delenv("ENABLE_LIVE_RAG", raising=False)

    # Send a question to the real RAG endpoint
    response = client.post(
        "/ask/rag",
        json={"question": "Where can I park my car?"}
    )

    # Verify that the safety switch blocks the request
    assert response.status_code == 503
    assert response.json()["detail"] == "Live AI mode is disabled."
