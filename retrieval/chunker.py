
from retrieval.loader import load_documents


def chunk_documents(documents):
    chunks = []

    for document in documents:
        # Split the document into paragraphs
        paragraphs = [
            part.strip()
            for part in document["content"].split("\n\n")
            if part.strip()
        ]

        if not paragraphs:
            continue

        # Preserve the document title for context
        title = (
            paragraphs[0]
            if paragraphs[0].startswith("# ")
            else ""
        )

        content_paragraphs = (
            paragraphs[1:] if title else paragraphs
        )

        for index, paragraph in enumerate(content_paragraphs, start=1):
            chunks.append({
                "id": f"{document['source']}#chunk-{index}",
                "source": document["source"],
                "content": f"{title}\n{paragraph}".strip()
            })

    return chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents)

    for chunk in chunks:
        print(f"\nID: {chunk['id']}")
        print(chunk["content"])

    print(f"\nTotal chunks: {len(chunks)}")
