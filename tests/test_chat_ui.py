
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


def test_live_ai_config_disabled(monkeypatch):
    monkeypatch.delenv("ENABLE_LIVE_RAG", raising=False)

    response = client.get("/chat/config")

    assert response.status_code == 200
    assert response.json()["live_rag_enabled"] is False


def test_live_ai_config_enabled(monkeypatch):
    monkeypatch.setenv("ENABLE_LIVE_RAG", "true")

    response = client.get("/chat/config")

    assert response.status_code == 200
    assert response.json()["live_rag_enabled"] is True


def test_real_ai_option_exists_but_starts_disabled():
    response = client.get("/chat")

    assert response.status_code == 200

    html = response.text

    assert 'value="live-rag" disabled' in html
    assert '"/chat/config"' in html
    assert '"/ask/rag"' in html
