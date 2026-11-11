from retrieval.loader import load_documents
from retrieval.chunker import chunk_documents


def test_parking_chunk():
    documents = load_documents()
    chunks = chunk_documents(documents)

    assert any(
        chunk["source"] == "parking.md"
        for chunk in chunks
    )