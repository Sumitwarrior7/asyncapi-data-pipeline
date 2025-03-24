import re
from typing import List, Dict
from utils import call_ollama

def clean_text(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int) -> List[Dict]:
    text = clean_text(text)
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size:
            chunks.append({"text": current_chunk.strip()})
            current_chunk = sentence
        else:
            current_chunk += " " + sentence
    
    if current_chunk:
        chunks.append({"text": current_chunk.strip()})
    
    return chunks

def filter_chunks(chunks: List[Dict], config: Dict) -> List[Dict]:
    filtered = []
    for chunk in chunks:
        prompt = f"""Classify this text as (1) useful content or (0) metadata/boilerplate:
        {chunk['text'][:500]}
        Answer only 1 or 0:"""
        
        response = call_ollama(prompt, config).strip()
        if response == "1":
            filtered.append(chunk)
    return filtered
