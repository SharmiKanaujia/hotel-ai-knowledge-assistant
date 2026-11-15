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
