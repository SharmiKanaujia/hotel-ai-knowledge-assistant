import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Hotel AI Assistant!"
    }
def test_check_in_question():
    response = client.post(
        "/ask",
        json={"question": "What time is check-in?"}
    )

    assert response.status_code == 200
    assert response.json()["source"] == "FAQ001"
    assert response.json()["answer"] == "Check-in begins at 3:00 PM."


def test_unknown_question():
    response = client.post(
        "/ask",
        json={"question": "Does the hotel have a swimming pool?"}
    )

    assert response.status_code == 200
    assert response.json()["source"] is None
    assert response.json()["answer"] == "I could not find that information."

def test_breakfast_question():
    response = client.post(
        "/ask",
        json={"question": "What time is the breakfast?"}
    )
    assert response.status_code == 200
    assert response.json()["source"] == "FAQ003"
    assert "7:00 AM" in response.json()["answer"]

def test_missing_question():
    response = client.post("/ask", json={})

    assert response.status_code == 422


def test_early_checkin_policy_unknown():
    response = client.post(
        "/ask",
        json={"question": "Can I check in early at 10 AM?"}
    )

    assert response.status_code == 200
    assert response.json()["source"] is None
    assert response.json()["answer"] == "I could not find that information."

@pytest.mark.xfail(
    reason="Keyword matching cannot distinguish early check-in from normal check-in",
    strict=True
)
def test_early_checkin_policy_unknown():
    response = client.post(
        "/ask",
        json={"question": "Can I check in early at 10 AM?"}
    )

    assert response.status_code == 200
    assert response.json()["source"] is None
    assert response.json()["answer"] == "I could not find that information."

@pytest.mark.xfail(
    reason="Keyword matching cannot distinguish early check-in from normal check-in",
    strict=True
)
def test_breakfast_price_policy_unknown():
    response = client.post(
        "/ask",
        json={"question": "Is breakfast free?"}
    )

    assert response.status_code == 200
    assert response.json()["source"] is None
    assert response.json()["answer"] == "I could not find that information."

