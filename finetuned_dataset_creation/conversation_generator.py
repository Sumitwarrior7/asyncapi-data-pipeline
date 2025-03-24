from utils import call_ollama
from typing import Dict
import random

def generate_conversation(qa: Dict, config: Dict) -> Dict:
    base = [
        {"from": "human", "value": qa["question"]},
        {"from": "gpt", "value": qa["answer"]}
    ]
    
    if random.random() > 0.7:
        prompt = f"""Create a conversation about: {qa['question']}
        Include 2-3 turns. Format:
        User: ...
        Assistant: ..."""
        
        response = call_ollama(prompt, config)
        return parse_conversation(response)
    
    return {"conversations": base}

def parse_conversation(text: str) -> Dict:
    turns = []
    current_role = None
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith("User:"):
            turns.append({"from": "human", "value": line[5:].strip()})
        elif line.startswith("Assistant:"):
            turns.append({"from": "gpt", "value": line[10:].strip()})
    return {"conversations": turns} if len(turns) >=2 else None
