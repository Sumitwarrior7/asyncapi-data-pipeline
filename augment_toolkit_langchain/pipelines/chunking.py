from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def chunk_document(text: str) -> list[str]:
    """Split text into manageable chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=int(os.getenv("CHUNK_SIZE", 1500)),
        chunk_overlap=200,
        separators=["\n\n", "\n", " "]
    )
    return splitter.split_text(text)
