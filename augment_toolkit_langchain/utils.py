import os
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

def save_output(data: List[Dict], filename: str = "dataset.jsonl"):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{filename}", "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")

def load_documents(input_dir: str = "input") -> List[str]:
    documents = []
    for file in os.listdir(input_dir):
        if file.endswith(".txt"):
            with open(os.path.join(input_dir, file), "r") as f:
                documents.append(f.read())
    return documents
