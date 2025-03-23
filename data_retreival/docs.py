import os
import markdown2
import yaml
from bs4 import BeautifulSoup
from tqdm import tqdm
from preprocessing import preprocess_html

# Constants
GITHUB_ORG = "https://api.github.com/orgs/asyncapi/repos"
OUTPUT_DIR = "asyncapi_data"
DOC_EXTENSIONS = {".md", ".yaml", ".yml", ".json"}  # Documentation files


def extract_docs(repo_path, repo_name):
    """Extract and structure documentation-related files from repositories."""
    extracted_docs = []
    
    for root, _, files in os.walk(repo_path):
        depth_rank = root[len(repo_path):].count(os.sep)  # Calculate depth rank
        
        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file_extension in DOC_EXTENSIONS:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, repo_path)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Convert markdown to plain text
                    if file_extension == ".md":
                        content = markdown2.markdown(content)
                    
                    # Parse YAML/JSON
                    elif file_extension in {".yaml", ".yml"}:
                        try:
                            content = yaml.safe_load(content)
                        except Exception:
                            continue  # Skip if YAML parsing fails

                    # Preprocessing the html content of .md file
                    preprocessed_content = str(content)
                    if file_extension == ".md":
                        preprocessed_content = preprocess_html(preprocessed_content)
                    
                    extracted_docs.append({
                        "repo_name": repo_name,
                        "file_name": file,
                        "file_extension": file_extension,
                        "file_path": relative_path,
                        "depth_rank": depth_rank,
                        "content": preprocessed_content
                    })
    
    return extracted_docs