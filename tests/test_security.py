from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_reject_empty_question():
    response = client.post(
        "/ask",
        json={"question": ""}
    )

    assert response.status_code == 422


def test_reject_oversized_question():
    response = client.post(
        "/ask",
        json={"question": "A" * 501}
    )

    assert response.status_code == 422

def test_reject_whitespace_only_question():
    response = client.post(
        "/ask",
        json={"question": "     "}
    )

    assert response.status_code == 422


def test_accept_exactly_500_characters():
    response = client.post(
        "/ask",
        json={"question": "A" * 500}
    )

    assert response.status_code == 200