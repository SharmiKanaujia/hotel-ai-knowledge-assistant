
import os
import boto3

from rag.pipeline import prepare_rag


def generate_answer(question: str, client=None):
    # Find relevant hotel information
    rag_data = prepare_rag(question)

    # Use an existing client for tests, or create
    # a real AWS Bedrock client
    if client is None:
        client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv(
                "AWS_REGION", "ap-northeast-1"
            )
        )

    # Send our RAG prompt to the language model
    response = client.converse(
        modelId=os.getenv(
            "BEDROCK_MODEL_ID",
            "amazon.nova-lite-v1:0"
        ),
        messages=[
            {
                "role": "user",
                "content": [
                    {"text": rag_data["prompt"]}
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 256,
            "temperature": 0
        }
    )

    # Extract the model's answer
    answer = "".join(
        block.get("text", "")
        for block in response["output"]["message"]["content"]
    ).strip()

    return {
        "question": question,
        "answer": answer or "I could not find that information.",
        "sources": rag_data["sources"]
    }


if __name__ == "__main__":
    result = generate_answer(
        "Where can I leave my car?"
    )

    print(result)
