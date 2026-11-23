from unittest.mock import patch
from retrieval.semantic import get_embedding_model
from retrieval.search import search_documents
from retrieval.semantic import search_semantic


def test_semantic_search_finds_parking():
    question = "Where can I leave my car?"

    keyword_results = search_documents(question)
    semantic_results = search_semantic(question, top_k=3)

    # Keyword search cannot find the answer
    assert keyword_results == []

    # Semantic search should find relevant documents
    assert len(semantic_results) > 0

    # Parking should be the most relevant document
    assert semantic_results[0]["source"] == "parking.md"


def test_semantic_search_filters_unrelated_documents():
    results = search_semantic(
        "Does the hotel provide a free airport shuttle?"
    )

    assert results == []


def test_semantic_search_keeps_relevant_breakfast_documents():
    results = search_semantic(
        "What time is breakfast served?"
    )

    assert len(results) > 0
    assert all(r["source"] == "dining.md" for r in results)

def test_embedding_model_is_cached():
    get_embedding_model.cache_clear()

    try:
        with patch("retrieval.semantic.TextEmbedding") as mock_model:
            first_model = get_embedding_model()
            second_model = get_embedding_model()

            # Both calls should return the same object
            assert first_model is second_model

            # The model should be initialized only once
            mock_model.assert_called_once_with(
                model_name="BAAI/bge-small-en-v1.5"
            )
    finally:
        get_embedding_model.cache_clear()
