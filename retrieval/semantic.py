
import numpy as np
from fastembed import TextEmbedding

from retrieval.loader import load_documents
from retrieval.chunker import chunk_documents


def search_semantic(
    question,
    top_k=3,
    min_score=0.65,
    score_margin=0.10
):
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
        # No results above our minimum relevance score
    if len(best_indices) == 0:
        return []

    top_score = float(scores[best_indices[0]])

    if top_score < min_score:
        return []

    # Keep only strong matches close to the best result
    best_indices = [
        i for i in best_indices
        if float(scores[i]) >= min_score
        and top_score - float(scores[i]) <= score_margin
    ]
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