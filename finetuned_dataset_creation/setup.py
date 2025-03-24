import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def setup():
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    small_model = os.getenv("SMALL_MODEL_NAME")
    large_model = os.getenv("LARGE_MODEL_NAME")
    ollama_url = os.getenv("OLLAMA_URL")
    
    if not os.path.exists("config.yaml"):
        default_config = {
            "chunk_size": 1500,
            "model_name": small_model,
            "base_url": ollama_url,
            "temperature": 0.5,
            "max_tokens": 512
        }
        with open("config.yaml", "w") as f:
            yaml.dump(default_config, f)
    
    print("Setup complete. Add text files to input/ and run: python main.py")

if __name__ == "__main__":
    setup()
