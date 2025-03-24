from utils import call_ollama
from typing import List, Dict

def generate_questions(chunk: Dict, config: Dict) -> List[Dict]:
    prompt = f"""Generate 3 questions about this text. Use numbered format:
    Text: {chunk['text']}
    Questions:"""
    
    response = call_ollama(prompt, config)
    questions = [q.split(') ')[1] for q in response.split('\n') if q.strip()][:3]
    
    return [{
        "question": q,
        "context": chunk['text']
    } for q in questions]

def generate_answers(qa_pairs: List[Dict], config: Dict) -> List[Dict]:
    for pair in qa_pairs:
        prompt = f"""Answer this question using only the context:
        Context: {pair['context']}
        Question: {pair['question']}
        Answer:"""
        
        pair["answer"] = call_ollama(prompt, config).strip()
    return qa_pairs

def validate_qa(qa_pairs: List[Dict], config: Dict) -> List[Dict]:
    valid = []
    for pair in qa_pairs:
        prompt = f"""Verify this Q&A pair (1=valid/0=invalid):
        Context: {pair['context']}
        Q: {pair['question']}
        A: {pair['answer']}
        Answer:"""
        
        if call_ollama(prompt, config).strip() == "1":
            valid.append(pair)
    return valid
