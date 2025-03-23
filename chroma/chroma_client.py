import chromadb
from datetime import datetime


# Example setup of the client to connect to your chroma server
client = chromadb.HttpClient(host='localhost', port=8000)

# Or for async usage:
# async def main():
#     client = await chromadb.AsyncHttpClient(host='localhost', port=8000)


# collection = client.create_collection(
#     name="first_collection", 
#     metadata={
#         "hnsw:space": "cosine",
#         "hnsw:search_ef": 100
#     }
# )

collection = client.get_collection(name="new_name")
# collection.modify(name="new_name")

# Adding data
# docs = ["Document 1", "Document 2"]
# metadatas = [{"category": "A"}, {"category": "B"}]
# ids = ["doc1", "doc2"]
def add_data(collection, docs, metadatas, ids):
    collection.add(
        documents=docs, 
        metadatas=metadatas, 
        ids=ids
    )

def update_data(collection, new_ids, new_documents):
    collection.update(
        ids=new_ids,
        # embeddings=embddings,
        # metadatas=metadatas,
        documents=new_documents,
    )

# Chroma also supports an upsert operation, which updates existing items, or adds them if they don't yet exist.
def upsert_data(collection, new_ids, new_documents):
    collection.upsert(
        ids=new_ids,
        # embeddings=embddings,
        # metadatas=metadatas,
        documents=new_documents,
    )

def delete_data(collection, ids):
    collection.delete(
        ids=ids,
        # where={"chapter": "10000"}
    )

def get_data_by_ids(collection, ids):
    data = collection.get(
        ids=ids,
        # where={"style": "style1"}
    )
    return data

def query_data_by_query_texts(collection, query_texts, n_results):
    data = collection.query(
        query_texts=query_texts,
        n_results=n_results,
        # include=["uris", "documents"],
        # where={"metadata_field": "is_equal_to_this"},
        # where_document={"$contains":"search_string"}
    )
    return data

# docs = ["Document 2 got updated", "Brand new Document 4"]
# ids = ["id4"]
# delete_data(collection, ids)
data = query_data_by_query_texts(collection, ["I am Multi billionaire Sumit Ghosh"], 1)
print("data :", data)


# pd = collection.peek() 
# cnt = collection.count() 
# print(f"this is {pd}   OR   this is cnt {cnt}")
    