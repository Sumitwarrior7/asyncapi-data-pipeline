import chromadb
from chromadb.utils import embedding_functions

# Connect to the ChromaDB server
# client = chromadb.HttpClient(host='localhost', port=8000)
# collection_name = "video_metadata"

# Get embedding function
def get_embedding_function():
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return sentence_transformer_ef

# Create or get a collection
def get_or_create_collection(client, collection_name):
    emb_fn = get_embedding_function()
    collection = client.get_or_create_collection(
        name=collection_name, 
        embedding_function=emb_fn
    )
    return collection

# ================================
# Function to add videos data
# ================================
def add_video_data(collection, video_list):
    ids = [video["video_id"] for video in video_list]  # Unique video IDs
    documents = [video["transcript"] for video in video_list]  # Store transcript as document
    metadatas = [{  # Store video metadata
        "title": video["title"],
        "description": video["description"],
        "length": video["length"],
        "upload_date": video["upload_date"],
        "uploader": video["uploader"]
    } for video in video_list]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

# ================================
# Function to add code data
# ================================
def add_code_data(collection, code_list):
    ids = [f"{code['repo_name']}/{code['file_path']}" for code in code_list]  # Unique ID: repo + file path
    documents = [code["content"] for code in code_list]  # Store file content
    metadatas = [{  # Store file metadata
        "repo_name": code["repo_name"],
        "file_name": code["file_name"],
        "file_extension": code["file_extension"],
        "file_path": code["file_path"],
        "depth_rank": code["depth_rank"],
    } for code in code_list]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)

# ================================
# Function to add blog data
# ================================
def add_blog_data(collection, blog_list):
    ids = [blog["id"] for blog in blog_list]  # Unique blog IDs
    documents = [blog["content"] for blog in blog_list]  # Store full blog content
    metadatas = [{  # Store blog metadata
        "title": blog["title"],
        "link": blog["link"],
        "summary": blog["summary"]
    } for blog in blog_list]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)

# ================================
# Function to add docs data
# ================================
def add_docs_data(collection, docs_list):
    ids = [f"{doc['repo_name']}/{doc['file_path']}" for doc in docs_list]  # Unique ID: repo + file path
    documents = [doc["content"] for doc in docs_list]  # Store document content
    metadatas = [{  # Store document metadata
        "repo_name": doc["repo_name"],
        "file_name": doc["file_name"],
        "file_extension": doc["file_extension"],
        "file_path": doc["file_path"],
        "depth_rank": doc["depth_rank"],
    } for doc in docs_list]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)

# Function to update existing video data
def update_video_data(collection, video_list):
    ids = [video["video_id"] for video in video_list]
    documents = [video["transcript"] for video in video_list]
    metadatas = [{
        "title": video["title"],
        "description": video["description"],
        "length": video["length"],
        "upload_date": video["upload_date"],
        "uploader": video["uploader"]
    } for video in video_list]

    collection.update(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

# Function to upsert video data (update if exists, add if not)
def upsert_video_data(collection, video_list):
    ids = [video["video_id"] for video in video_list]
    documents = [video["transcript"] for video in video_list]
    metadatas = [{
        "title": video["title"],
        "description": video["description"],
        "length": video["length"],
        "upload_date": video["upload_date"],
        "uploader": video["uploader"]
    } for video in video_list]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

# Function to delete video data
def delete_data(collection, ids):
    collection.delete(ids=ids)

# Function to get video data by IDs
def get_data_by_ids(collection, ids):
    return collection.get(ids=ids)

# Function to query video data by text similarity (search in transcript)
def query_by_text(collection, query_text, n_results=3):
    return collection.query(query_texts=[query_text], n_results=n_results)



# Example video data
video_data_sample = [{
    "video_id": "12345",
    "title": "Introduction to AI",
    "description": "A basic introduction to AI concepts.",
    "length": "10:30",
    "upload_date": "2024-03-01",
    "uploader": "Tech Channel",
    "transcript": "AI is transforming the world..."
}]

# Store the sample video data
# add_video_data(collection, video_data_sample)

# Query example
query = """
Later in the year, I thought it would be a great idea to bring back the online conference to provide an opportunity for those who can't travel but still want to speak and share their expertise. This idea completed the entire experience, bringing the total number of events to four.
"""
client = chromadb.HttpClient(host='localhost', port=8000)
faaltu_collection = get_or_create_collection(client, "blogs_data")
# add_video_data(faaltu_collection, video_data_sample)
query_result = query_by_text(faaltu_collection, query, n_results=2)
print("Query Result:", query_result)
