import os
import requests
# import git
import shutil
import json
import markdown2
import yaml
from bs4 import BeautifulSoup
from tqdm import tqdm
# import chromadb
import feedparser
from data_retreival.repos import get_repos, clone_repo 
from data_retreival.blog import fetch_blogs
from data_retreival.docs import extract_docs
from data_retreival.code_files import extract_code_data
from data_retreival.videos import get_channel_videos_data
from storage.mongo_storage import get_mongo_connection, create_collections, store_data, fetch_and_modify_docs, store_coding_data, fetch_all_data
# from storage.chroma_storage import get_or_create_collection, add_video_data, add_blog_data, add_code_data, add_docs_data


# -------------------Not important-------------------
# def save_blogs_to_txt(data_list, file_name):
#     """
#     Convert a list of dictionaries into a formatted text string and save it to a text file.
    
#     :param data_list: List of dictionaries containing blog data.
#     :param file_name: Name of the output text file.
#     """
#     with open(file_name, "w", encoding="utf-8") as file:
#         file.write("AsyncAPI Blogs Data\n\n")
#         file.write("="*80 + "\n\n")
        
#         for index, entry in enumerate(data_list, start=1):
#             formatted_entry = (
#                 f"Post {index}\n"
#                 f"ID: {entry.get('id', 'N/A')}\n"
#                 f"Title: {entry.get('title', 'No Title')}\n"
#                 f"Link: {entry.get('link', 'No Link')}\n"
#                 f"Summary: {entry.get('summary', 'No Summary')}\n"
#                 f"Content:\n\"\"\"\n{entry.get('content', 'No Content')}\n\"\"\"\n"
#                 f"{'-'*80}\n\n\n"
#             )
#             file.write(formatted_entry)

# def save_docs_to_txt(data_list, file_name):
#     """
#     Convert a list of dictionaries into a formatted text string and save it to a text file.
    
#     :param data_list: List of dictionaries containing file metadata.
#     :param file_name: Name of the output text file.
#     """
#     with open(file_name, "w", encoding="utf-8") as file:
#         file.write("Repository File Data\n\n")
#         file.write("="*80 + "\n\n")
        
#         for entry in data_list:
#             formatted_entry = (
#                 f"Repository Name: {entry.get('repo_name', 'N/A')}\n"
#                 f"File Name: {entry.get('file_name', 'No File Name')}\n"
#                 f"File Extension: {entry.get('file_extension', 'No Extension')}\n"
#                 f"File Path: {entry.get('file_path', 'No Path')}\n"
#                 f"Depth Rank: {entry.get('depth_rank', 'N/A')}\n"
#                 f"Content:\n{entry.get('content', 'No Content')}\n"
#                 f"{'-'*80}\n\n"
#             )
#             file.write(formatted_entry)
# -------------------Not important-------------------

def main():
    """Main pipeline to fetch blogs, repos, and store data."""
    # os.makedirs(OUTPUT_DIR, exist_ok=True)
    # os.makedirs("repos", exist_ok=True)

    # Connect to the Mongodb server
    db = get_mongo_connection()
    # fetch_and_modify_docs(db)
    # create_collections(db, ["blogs", "docs", "codeFiles", "youtubeFiles"])

    # Connect to the ChromaDB local server 
    # client = chromadb.HttpClient(host='localhost', port=8000)
    # videos_collection = get_or_create_collection(client, "videos_data")
    # blogs_collection = get_or_create_collection(client, "blogs_data")
    # docs_collection = get_or_create_collection(client, "docs_data")
    # codes_collection = get_or_create_collection(client, "codes_data")
    
    print("📥 Fetching blogs...")
    blogs = fetch_blogs()
    store_data(db, "blogs", blogs)

    # print("📥 Fetching GitHub repositories...")
    # repos = get_repos()

    # all_docs = []
    # all_code_files = []
    # for repo_url in tqdm(repos, desc="Processing Repositories"):
    #     repo_name = repo_url.split("/")[-1].replace(".git", "")
    #     print(f"\nCloning {repo_name}...")
        
    #     repo_path = clone_repo(repo_url, repo_name)
    #     # docs = extract_docs(repo_path, repo_name)
    #     # for doc in docs:
    #     #     all_docs.append(doc)
    #     # print("docs :", docs)
    #     code_files = extract_code_data(repo_path, repo_name)
    #     for fl in code_files:
    #         all_code_files.append(fl)
    #     shutil.rmtree(repo_path)  # Cleanup repo after extraction
    #     print(f"\nCloning Finished!!!!!!")

    # print("\n✅ Data extraction complete! All content is stored in MongoDB.")
    # Storing data in mongodb
    # store_coding_data(db, "codeFiles", all_code_files)
    # store_data(db, "docs", all_docs)


    # ----------Getting details of youtube videos of a channel----------
    # channel_url = "https://www.youtube.com/@AsyncAPI"
    # api_key = "add_your_own_key"
    # videos_data = get_channel_videos_data(channel_url, api_key)

    # Store the youtube video data into chromadb local server
    # add_video_data(videos_collection, videos_data)

    # Store the youtube video data into mongodb instance
    # store_data(db, "youtubeFiles", videos_data)

    

if __name__ == "__main__":
    main()
