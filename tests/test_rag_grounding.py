
from rag.pipeline import prepare_rag


def test_rag_prompt_requires_grounded_answers(monkeypatch):

    # Simulate finding a hotel parking document
    def fake_search_semantic(question, top_k=3):
        return [
            {
                "id": "parking.md#chunk-1",
                "source": "parking.md",
                "content": "Parking is available."
            }
        ]

    monkeypatch.setattr(
        "rag.pipeline.search_semantic",
        fake_search_semantic
    )

    result = prepare_rag("Where can I park my car?")

    # Verify hotel knowledge is included
    assert "Parking is available." in result["prompt"]

    # Verify our grounding instructions exist
    assert "Do not assume or invent details" in result["prompt"]
    assert "Do not add suggestions or extra information" in result["prompt"]

    # Verify the source
    assert result["sources"] == ["parking.md"]
