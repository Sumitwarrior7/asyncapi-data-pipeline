import os
import requests
import git
import shutil
from bs4 import BeautifulSoup
from tqdm import tqdm
from preprocessing import preprocess_html

# Constants
GITHUB_ORG = "https://api.github.com/orgs/asyncapi/repos"

def get_repos():
    """Fetch all AsyncAPI repositoriy urls from GitHub."""
    repos = []
    page = 1

    while True:
        response = requests.get(GITHUB_ORG, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            print("Failed to fetch repositories.")
            break
        
        data = response.json()
        if not data:
            break  # No more pages

        repos.extend(data)
        page += 1  # Move to the next page

    return [repo["clone_url"] for repo in repos]


def clone_repo(repo_url, repo_name):
    """Clone a GitHub repository."""
    repo_path = os.path.join("repos", repo_name)
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)  # Remove existing directory

    git.Repo.clone_from(repo_url, repo_path)
    return repo_path