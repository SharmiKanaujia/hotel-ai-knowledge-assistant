
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_rag_demo_parking(monkeypatch):
    monkeypatch.setenv("ENABLE_DEMO_RAG", "true")

    response = client.post(
        "/ask/rag/demo",
        json={"question": "Where can I park my car?"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Parking is available."
    assert response.json()["sources"] == ["parking.md"]


def test_rag_demo_unknown(monkeypatch):
    monkeypatch.setenv("ENABLE_DEMO_RAG", "true")

    response = client.post(
        "/ask/rag/demo",
        json={"question": "Where is the swimming pool?"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "I could not find that information."
    assert response.json()["sources"] == []


def test_rag_demo_disabled_by_default(monkeypatch):
    monkeypatch.delenv("ENABLE_DEMO_RAG", raising=False)

    response = client.post(
        "/ask/rag/demo",
        json={"question": "Where can I park my car?"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Demo AI mode is unavailable."
