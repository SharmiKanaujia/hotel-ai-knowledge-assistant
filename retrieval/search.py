
import re
from retrieval.loader import load_documents

STOP_WORDS = {"is", "the", "a", "at", "in", "what", "when",
              "does", "hotel", "can", "i", "time"}


def search_documents(question):
    documents = load_documents()

    # Convert the question into individual words
    question_words = set(
        re.findall(r"[a-z0-9]+", question.lower())
    ) - STOP_WORDS

    results = []

    for document in documents:
        content_words = set(
            re.findall(r"[a-z0-9]+", document["content"].lower())
        )

        # Count words appearing in both question and document
        score = len(question_words & content_words)

        if score > 0:
            results.append({
                "source": document["source"],
                "score": score,
                "content": document["content"]
            })

    # Put the most relevant documents first
    results.sort(key=lambda item: item["score"], reverse=True)

    return results


if __name__ == "__main__":
    matches = search_documents("What time is breakfast available?")

    for match in matches:
        print(f"Source: {match['source']}")
        print(f"Score: {match['score']}")
