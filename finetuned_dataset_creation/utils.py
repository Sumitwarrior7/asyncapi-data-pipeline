import os
import json
import time
import requests
from typing import List, Dict, Any
import ollama

def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_json(data: Any, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_jsonl(data: List[Dict], file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write("\n")

# def call_ollama(prompt: str, config: Dict) -> str:
#     for attempt in range(config["max_retries"]):
#         try:
#             response = requests.post(
#                 f"{config['base_url']}/chat/completions",
#                 json={
#                     "model": config["model_name"],
#                     "messages": [{"role": "user", "content": prompt}],
#                     "temperature": config["temperature"],
#                     "top_p": config["top_p"],
#                     "max_tokens": config["max_tokens"]
#                 },
#                 timeout=60
#             )
#             response.raise_for_status()
#             return response.json()["choices"][0]["message"]["content"]
#         except Exception as e:
#             print(f"Attempt {attempt+1} failed: {str(e)}")
#             time.sleep(config["retry_delay"])
#     return ""

def call_ollama(prompt: str, config: Dict) -> str:
    """
    Calls the Ollama LLM using the official Python API instead of manual HTTP requests.
    """
    for attempt in range(config.get("max_retries", 3)):  # Default to 3 retries
        try:
            response = ollama.chat(
                model=config["model_name"],
                messages=[{"role": "user", "content": prompt}],
                temperature=config.get("temperature", 0.5),
                max_tokens=config.get("max_tokens", 512)
            )
            return response['message']['content']
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {str(e)}")
            time.sleep(config.get("retry_delay", 2))  # Default retry delay = 2s
    return ""

def list_input_files():
    return [f for f in os.listdir("input") if f.endswith(".txt")]
