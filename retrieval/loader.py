
from pathlib import Path

# Locate the knowledge folder
KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


def load_documents():
    documents = []

    for file_path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "content": content
        })

    return documents


if __name__ == "__main__":
    for document in load_documents():
        print(f"Source: {document['source']}")
        print(document["content"])
