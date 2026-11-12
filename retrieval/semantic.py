
import numpy as np
from fastembed import TextEmbedding

from retrieval.loader import load_documents
from retrieval.chunker import chunk_documents


def search_semantic(question, top_k=3):
    chunks = chunk_documents(load_documents())

    if not chunks:
        return []

    model = TextEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    # Convert document chunks into numerical vectors
    texts = [chunk["content"] for chunk in chunks]
    vectors = np.array(list(model.passage_embed(texts)))

    # Convert the guest's question into a vector
    query_vector = list(model.query_embed(question))[0]

    # Compare the question with each chunk
    scores = vectors @ query_vector

    # Find the highest-scoring chunks
    best_indices = np.argsort(scores)[::-1][:top_k]

    return [
        {
            "id": chunks[int(i)]["id"],
            "source": chunks[int(i)]["source"],
            "score": float(scores[i]),
            "content": chunks[int(i)]["content"]
        }
        for i in best_indices
    ]


if __name__ == "__main__":
    results = search_semantic(
        "Where can I leave my car?"
    )

    for result in results:
        print(result["source"], round(result["score"], 3))