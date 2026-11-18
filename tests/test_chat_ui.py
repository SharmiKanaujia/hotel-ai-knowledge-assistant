
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

def test_chat_page_has_answer_modes():
    response = client.get("/chat")

    assert response.status_code == 200

    html = response.text

    # Check that the answer mode dropdown exists
    assert 'id="answer-mode"' in html

    # Check that both modes are available
    assert 'value="faq"' in html
    assert 'value="rag"' in html

    # Check that JavaScript knows the demo endpoint
    assert '"/ask/rag/demo"' in html
