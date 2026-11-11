from retrieval.search import search_documents


def test_breakfast_document_ranking():
    results = search_documents(
        "What time is breakfast available?"
    )

    assert len(results) > 0
    assert results[0]["source"] == "dining.md"
    assert results[0]["score"] == 2

def test_parking_document_ranking():
    results = search_documents(
        "What time is parking available?"
    )

    assert len(results) > 0
    assert results[0]["source"] == "parking.md"
    assert results[0]["score"] == 2

def test_unknown_document():
    results = search_documents(
        "Does the hotel offer a gym?"
    )

    assert results == []

def test_parking_chunk_retrieval():
    results = search_documents("Is parking available?")

    assert len(results) > 0
    assert results[0]["source"] == "parking.md"
    assert results[0]["id"] == "parking.md#chunk-2"
    assert "Parking is available." in results[0]["content"]
    