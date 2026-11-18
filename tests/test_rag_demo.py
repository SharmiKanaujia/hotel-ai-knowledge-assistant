
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_rag_demo_parking():
    response = client.post(
        "/ask/rag/demo",
        json={"question": "Where can I park my car?"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Parking is available."
    assert response.json()["sources"] == ["parking.md"]


def test_rag_demo_unknown():
    response = client.post(
        "/ask/rag/demo",
        json={"question": "Where is the swimming pool?"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "I could not find that information."
    assert response.json()["sources"] == []
