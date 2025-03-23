# AsyncAPI Data Pipelines

## Functionalities
* Fetch data from various sources like blogs, docs, codebases, YouTube videos, etc.
* Store and query the data from databases like MongoDB, ChromaDB.

## Installation Steps
1. Fork the repo locally.
2. Activate virtual environment.
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```
3. Install required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file with the following credentials:
   ```ini
   MONGO_USER=""
   MONGO_PASSWORD=""
   MONGO_CLUSTER_NAME=""
   ```
5. Run `main.py` to start the pipelines.

## Folder Structure
- **chroma/**: Creates and queries Chroma client.
- **storage/**: Contains functions for interacting with MongoDB and ChromaDB.
- **data_retrieval/**: Contains pipelines for fetching data from various sources.