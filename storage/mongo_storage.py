from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from preprocessing import preprocess_html
from gridfs import GridFS
import json
from bson import ObjectId
import os
from dotenv import load_dotenv


load_dotenv()

# MongoDB connection function
def get_mongo_connection(uri="mongodb://localhost:27017", db_name="asyncapi_db"):
    USER = os.getenv("MONGO_USER")
    PASSWORD = os.getenv("MONGO_PASSWORD")
    CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME")
    uri = f"mongodb+srv://{USER}:{PASSWORD}@async-api-finetune-data.wten6.mongodb.net/?retryWrites=true&w=majority&appName=async-api-finetune-data"
    # uri = f"mongodb+srv://{USER}:{PASSWORD}@billionairecluster.atbqt.mongodb.net/?retryWrites=true&w=majority&appName=BillionaireCluster"
    print(uri)
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[db_name]
    return db

# Function to create collections if required
def create_collections(db, collection_names):
    existing_collections = db.list_collection_names()
    for collection in collection_names:
        if collection not in existing_collections:
            db.create_collection(collection)

# Function to store data into MongoDB
def store_data(db, table_name, data):
    if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
        raise ValueError("Data must be a list of dictionaries")
    
    collection = db[table_name]
    if data:
        collection.insert_many(data)


# Function to fetch and modify "docs" collection
def fetch_and_modify_docs(db):
    collection = db["docs"]

    # Fetch all documents where file_extension is ".md"
    documents = collection.find({"file_extension": ".md"})

    for doc in documents:
        if "content" in doc:
            updated_content = preprocess_html(doc["content"])
            collection.update_one({"_id": doc["_id"]}, {"$set": {"content": updated_content}})

# Function to fetch all data from a specified collection (table)
def fetch_all_data(db, table_name):
    collection = db[table_name]
    data = list(collection.find({}))  # Fetch all documents
    return data  # Returns a list of dictionaries


# ---------------------GridFs------------------------

# Function to store data into MongoDB and GridFS
def store_coding_data(db, table_name, data):
    if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
        raise ValueError("Data must be a list of dictionaries")
    
    fs = GridFS(db)  # Initialize GridFS
    collection = db[table_name]

    processed_data = []
    for entry in data:
        content = entry.pop("content", None)  # Extract content field
        
        if content:
            # content = preprocess_html(content)  # Preprocess content
            content_id = fs.put(content.encode("utf-8"), filename="content")  # Store in GridFS
            entry["content_id"] = str(content_id)  # Store reference ID in MongoDB
        
        processed_data.append(entry)

    if processed_data:
        collection.insert_many(processed_data)

# Function to retrieve content from GridFS using content_id
def get_content_from_gridfs(db, content_id):
    fs = GridFS(db)
    content = fs.get(ObjectId(content_id)).read().decode("utf-8")
    return content

def delete_file_from_gridfs(db, content_id):
    fs = GridFS(db)
    
    try:
        fs.delete(ObjectId(content_id))  # Delete file and its chunks
        print(f"File with content_id {content_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting file: {e}")