# Run the chroma server with "chroma run --path ./chroma_persistent_data" (Use relative path syntax)


# this script sets up a persistent ChromaDB instance for vector storage.
import chromadb
import os

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))
# Set the path for ChromaDB storage
chroma_path = os.path.join(script_directory, "chroma_persistent_data")
# Ensure the directory exists
os.makedirs(chroma_path, exist_ok=True)


client = chromadb.PersistentClient(path=chroma_path)
client.heartbeat()