
from unittest.mock import Mock

from rag.llm import generate_answer


def test_generate_answer_with_mock_bedrock():
    # Pretend AWS returned this answer
    fake_client = Mock()

    fake_client.converse.return_value = {
        "output": {
            "message": {
                "content": [
                    {"text": "Parking is available."}
                ]
            }
        }
    }

    result = generate_answer(
        "Where can I leave my car?",
        client=fake_client
    )

    assert result["answer"] == "Parking is available."
    assert "parking.md" in result["sources"]

    # Confirm our hotel knowledge reached the LLM
    call_args = fake_client.converse.call_args.kwargs
    prompt = call_args["messages"][0]["content"][0]["text"]

    assert "Parking is available." in prompt
    assert fake_client.converse.call_count == 1
