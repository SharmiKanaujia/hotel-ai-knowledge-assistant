
import json
from pathlib import Path
from fastapi.testclient import TestClient
from main import app

# Step 1: Load our evaluation questions
file_path = Path(__file__).with_name("cases.json")

with file_path.open("r", encoding="utf-8") as file:
    cases = json.load(file)

# Step 2: Create an API test client
client = TestClient(app)

correct_count = 0

# Step 3: Evaluate each question
for case in cases:
    response = client.post(
        "/ask",
        json={"question": case["question"]}
    )

    actual = response.json()

    is_correct = (
        response.status_code == 200
        and actual["source"] == case["expected_source"]
        and actual["answer"] == case["expected_answer"]
    )

    if is_correct:
        correct_count += 1
        print(f"PASS: {case['id']}")
    else:
        print(f"FAIL: {case['id']}")
        print(f"  Question: {case['question']}")
        print(f"  Expected: {case['expected_answer']}")
        print(f"  Actual:   {actual['answer']}")

# Step 4: Calculate accuracy
total = len(cases)
accuracy = (correct_count / total * 100) if total else 0

print("\n--- Evaluation Results ---")
print(f"Correct: {correct_count}/{total}")
print(f"Accuracy: {accuracy:.2f}%")
