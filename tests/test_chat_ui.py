
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_chat_page_loads():
    response = client.get("/chat")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Hotel AI Copilot" in response.text
    assert 'id="chat-form"' in response.text
    assert 'id="messages"' in response.text
