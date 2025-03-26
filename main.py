import os
import requests
# import git
import shutil
import json
import markdown2
import yaml
import tiktoken
from bs4 import BeautifulSoup
from tqdm import tqdm
# import chromadb
import feedparser
from data_retreival.repos import get_repos, clone_repo 
from data_retreival.blog import fetch_blogs
from data_retreival.docs import extract_docs
from data_retreival.code_files import extract_code_data
from data_retreival.videos import get_channel_videos_data
from storage.mongo_storage import get_mongo_connection, create_collections, store_data, fetch_and_modify_docs, store_coding_data, fetch_all_data, store_list_data
from utils import save_blogs_to_txt, save_data_to_jsonl, save_docs_to_txt, load_jsonl, count_tokens, add_token_counts, split_content_into_chunks, format_content_chunks, filter_docs_jsonl, calculate_token_stats, generate_code_json_data
# from storage.chroma_storage import get_or_create_collection, add_video_data, add_blog_data, add_code_data, add_docs_data


def main():
    """Main pipeline to fetch blogs, repos, and store data."""
    # os.makedirs(OUTPUT_DIR, exist_ok=True)
    # os.makedirs("repos", exist_ok=True)

    # Connect to the Mongodb server
    db = get_mongo_connection()
    # fetch_and_modify_docs(db)
    # create_collections(db, ["blogs", "docs", "codeFiles", "youtubeFiles"])
    # create_collections(db, ["blogs_context"])

    # Connect to the ChromaDB local server 
    # client = chromadb.HttpClient(host='localhost', port=8000)
    # videos_collection = get_or_create_collection(client, "videos_data")
    # blogs_collection = get_or_create_collection(client, "blogs_data")
    # docs_collection = get_or_create_collection(client, "docs_data")
    # codes_collection = get_or_create_collection(client, "codes_data")
    
    print("📥 Fetching blogs...")
    # code_files = fetch_all_data(db, "codeFiles")
    # generate_code_json_data(code_files)
    # save_data_to_jsonl(docs, "docs", "docs")
    # data_list = load_jsonl("blogs_final.jsonl")
    # chunked_data_list = split_content_into_chunks(data_list)
    # required_contexts = format_content_chunks(chunked_data_list)

    # -----------------Calcualting tokens for docs-----------------
    # docs_data_list = load_jsonl("docs.jsonl")
    # new_data_list = add_token_counts(data_list=docs_data_list)
    # save_data_to_jsonl(new_data_list, "docs_final", "docs")
    # filter_docs_jsonl('docs_final.jsonl', 'docs_final_2.jsonl')
    # calculate_token_stats('docs_final_2.jsonl')

    # chunked_data_list = split_content_into_chunks(data_list)
    # required_contexts = format_content_chunks(chunked_data_list)
    # store_list_data(db, "blogs_context", required_contexts)
    # save_data_to_jsonl(docs, "docs", "docs")
    # new_data_list = add_token_counts(data_list=data_list)
    # save_data_to_jsonl(new_data_list, "blogs_final", "blogs")
    # blogs = fetch_blogs()
    # store_data(db, "blogs", blogs)



    print("📥 Fetching GitHub repositories...")
    repos = get_repos()
    # all_docs = []
    all_code_files = []
    for repo_url in tqdm(repos, desc="Processing Repositories"):
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        if repo_name in {"spec", "spec-json-schemas", "generator", "cli", "modelina"}:
            repo_path = clone_repo(repo_url, repo_name)
            print(f"\nCloning {repo_name}...  and here is repo path :{repo_path}")
            # docs = extract_docs(repo_path, repo_name)
            # for doc in docs:
            #     all_docs.append(doc)
            # print("docs :", docs)

            code_files = extract_code_data(repo_path, repo_name)
            for fl in code_files:
                all_code_files.append(fl)
            shutil.rmtree(repo_path)  # Cleanup repo after extraction
            print(f"\nCloning Finished!!!!!!")

    print("\n✅ Data extraction complete! All content is stored in MongoDB.")
    generate_code_json_data(all_code_files)
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
