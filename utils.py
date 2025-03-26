import json
import tiktoken
from bs4 import BeautifulSoup
from tqdm import tqdm
import tiktoken
import os


# -------------------Not important-------------------
def save_blogs_to_txt(data_list, file_name):
    """
    Convert a list of dictionaries into a formatted text string and save it to a text file.
    
    :param data_list: List of dictionaries containing blog data.
    :param file_name: Name of the output text file.
    """
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("AsyncAPI Blogs Data\n\n")
        file.write("="*80 + "\n\n")
        
        for index, entry in enumerate(data_list, start=1):
            formatted_entry = (
                f"Post {index}\n"
                f"ID: {entry.get('id', 'N/A')}\n"
                f"Title: {entry.get('title', 'No Title')}\n"
                f"Link: {entry.get('link', 'No Link')}\n"
                f"Summary: {entry.get('summary', 'No Summary')}\n"
                f"Content:\n\"\"\"\n{entry.get('content', 'No Content')}\n\"\"\"\n"
                f"{'-'*80}\n\n\n"
            )
            file.write(formatted_entry)

def save_docs_to_txt(data_list, file_name):
    """
    Convert a list of dictionaries into a formatted text string and save it to a text file.
    
    :param data_list: List of dictionaries containing file metadata.
    :param file_name: Name of the output text file.
    """
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("Repository File Data\n\n")
        file.write("="*80 + "\n\n")
        
        for entry in data_list:
            formatted_entry = (
                f"Repository Name: {entry.get('repo_name', 'N/A')}\n"
                f"File Name: {entry.get('file_name', 'No File Name')}\n"
                f"File Extension: {entry.get('file_extension', 'No Extension')}\n"
                f"File Path: {entry.get('file_path', 'No Path')}\n"
                f"Depth Rank: {entry.get('depth_rank', 'N/A')}\n"
                f"Content:\n{entry.get('content', 'No Content')}\n"
                f"{'-'*80}\n\n"
            )
            file.write(formatted_entry)
# -------------------Not important-------------------

def save_data_to_jsonl(data_list, file_name, file_type):
    """
    Save a list of dictionaries into a JSONL file, ensuring only specified fields are included.
    
    :param data_list: List of dictionaries containing blog data.
    :param file_name: Name of the output JSONL file (without extension).
    """
    file_name = f"{file_name}.jsonl"
    blogs_fields_to_include = {"id", "title", "link", "summary", "content", "token_cnt"}  # Define required fields
    docs_fields_to_include = {"id", "repo_name", "file_name", "file_extension", "file_path", "depth_rank", "content", "token_cnt"}  # Define required fields
    fields_to_include = {}
    if file_type == "docs":
        fields_to_include = docs_fields_to_include
    elif file_type == "blogs":
        fields_to_include = blogs_fields_to_include
    
    with open(file_name, "w", encoding="utf-8") as file:
        for entry in data_list:
            filtered_entry = {key: entry[key] for key in fields_to_include if key in entry}  # Filter required fields
            json.dump(filtered_entry, file, ensure_ascii=False)
            file.write("\n") 

def filter_docs_jsonl(input_file, output_file):
    valid_extensions = {".md", ".yaml", ".yml", ".json", ".txt"}
    excluded_files = {
        "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "npm-shrinkwrap.json",
        ".eslintrc.json", ".prettierrc.json", "tsconfig.json", "babel.config.json",
        ".editorconfig", ".dockerignore"
    }
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                data = json.loads(line.strip())  # Parse JSON line
                file_extension = data.get("file_extension", "")  # Get file extension
                file_name = data.get("file_name", "")  # Get file name
                
                if file_extension in valid_extensions and file_name not in excluded_files:
                    json.dump(data, outfile)
                    outfile.write("\n")  # Write filtered JSON
            except json.JSONDecodeError:
                print("Skipping invalid JSON line")

def calculate_token_stats(input_file):
    max_tokens = float('-inf')
    min_tokens = float('inf')
    max_token_file = None
    min_token_file = None
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            try:
                data = json.loads(line.strip())  # Parse JSON line
                token_count = data.get("token_cnt", 0)  # Get token count
                file_name = data.get("file_name", "Unknown")
                file_extension = data.get("file_extension", "Unknown")
                
                if token_count > max_tokens:
                    max_tokens = token_count
                    max_token_file = (file_name, file_extension)
                
                if token_count < min_tokens:
                    min_tokens = token_count
                    min_token_file = (file_name, file_extension)
            except json.JSONDecodeError:
                print("Skipping invalid JSON line")
    
    print(f"Max Tokens: {max_tokens}, File: {max_token_file[0]}, Extension: {max_token_file[1]}")
    print(f"Min Tokens: {min_tokens}, File: {min_token_file[0]}, Extension: {min_token_file[1]}")
    
    return max_tokens, min_tokens

def load_jsonl(file_name):
    """
    Load data from a JSONL file into a list of dictionaries.
    
    :param file_name: Name of the JSONL file.
    :return: List of dictionaries containing the data.
    """
    data = []
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            data.append(json.loads(line))  # Convert JSON string to dictionary
    return data

def count_tokens(text, model="gpt-3.5-turbo"):
    """Count the number of tokens in a given text using OpenAI's tokenizer."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def add_token_counts(data_list, model="gpt-3.5-turbo"):
    """Takes a list of dictionaries, counts tokens in the 'content' field, and adds 'token_cnt'."""
    for entry in data_list:
        if "content" in entry:
            entry["token_cnt"] = count_tokens(entry["content"], model)
    return data_list

def split_content_into_chunks(data_list, chunk_size=2000, model="gpt-3.5-turbo"):
    """
    Splits the 'content' field of each dictionary in the data_list into chunks of specified token size
    and adds these chunks as a list under the key 'content_list'.

    :param data_list: List of dictionaries containing at least 'token_cnt' and 'content' fields.
    :param chunk_size: Number of tokens per chunk. Default is 2000.
    :param model: The model identifier for the tokenizer. Default is "gpt-3.5-turbo".
    :return: The updated list with 'content_list' added to each dictionary.
    """
    # Initialize the tokenizer
    encoding = tiktoken.encoding_for_model(model)

    for entry in data_list:
        if "content" in entry and "token_cnt" in entry:
            content = entry["content"]
            token_cnt = entry["token_cnt"]

            # Tokenize the content
            tokens = encoding.encode(content)

            # Split tokens into chunks of size chunk_size
            content_chunks = [
                encoding.decode(tokens[i:i + chunk_size])
                for i in range(0, token_cnt, chunk_size)
            ]

            # Add the list of content chunks to the dictionary
            entry["content_list"] = content_chunks

    return data_list

def format_content_chunks(data_list):
    """
    Formats each chunk in the 'content_list' of each dictionary in the data_list.

    :param data_list: List of dictionaries containing 'content_list' and other metadata.
    :return: List of formatted strings for each content chunk.
    """
    formatted_entries = []
    for index, entry in enumerate(data_list, start=1):
        content_chunks = entry.get('content_list', [])
        for chunk_number, chunk_content in enumerate(content_chunks, start=1):
            formatted_entry = (
                f"### Chunked Blog Post Data ###\n"
                f"Chunk Number: {chunk_number}\n"
                f"Post Index: {index}\n"
                f"----------------------------------------\n"
                f"ID: {entry.get('id', 'N/A')}\n"
                f"Title: {entry.get('title', 'No Title')}\n"
                f"Link: {entry.get('link', 'No Link')}\n"
                f"Summary: {entry.get('summary', 'No Summary')}\n"
                f"----------------------------------------\n"
                f"Chunk Content Start:\n\"\"\"\n{chunk_content}\n\"\"\"\n"
                f"Chunk Content End\n"
                f"========================================\n\n"
            )
            formatted_entries.append(formatted_entry)

    return formatted_entries

def generate_code_json_data(input_data):
    """Generate folder 'code_json_data' and create files for specific repositories."""
    folder_name = "code_json_data"
    os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist

    file_mapping = {
        "spec": "spec.jsonl",
        "spec-json-schemas": "spec-json-schemas.jsonl",
        "generator": "generator.jsonl",
        "cli": "cli.jsonl",
        "modelina": "modelina.jsonl"
    }
    
    file_paths = {repo: os.path.join(folder_name, filename) for repo, filename in file_mapping.items()}
    file_handlers = {repo: open(path, "a", encoding="utf-8") for repo, path in file_paths.items()}
    
    fields_to_include = {"id", "repo_name", "file_name", "file_extension", "file_path", "depth_rank", "content", "token_cnt"}
    
    try:
        for data in input_data:
            repo_name = data.get("repo_name")
            if repo_name in file_mapping:
                data["token_cnt"] = count_tokens(data.get("content", ""))
                filtered_data = {key: data[key] for key in fields_to_include if key in data}
                json.dump(filtered_data, file_handlers[repo_name])
                file_handlers[repo_name].write("\n")
    finally:
        for handler in file_handlers.values():
            handler.close()
            