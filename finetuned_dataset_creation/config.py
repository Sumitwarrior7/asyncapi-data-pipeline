import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, config_path=None):
        os.makedirs("input", exist_ok=True)
        os.makedirs("output", exist_ok=True)
        small_model = os.getenv("SMALL_MODEL_NAME", "gemma3:1b")  
        large_model = os.getenv("LARGE_MODEL_NAME", "gemma3:4b")   
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
        
        self.default_config = {
            "chunk_size": 1500,
            "model_name": small_model,
            "base_url": ollama_url,
            "system_prompt": "You are a helpful AI assistant.",
            "temperature": 0.5,
            "top_p": 0.9,
            "max_tokens": 512,
            "max_retries": 3,
            "retry_delay": 2
        }
        
        self.config = self.default_config.copy()
        
        if config_path and Path(config_path).exists():
            with open(config_path, "r") as f:
                user_config = yaml.safe_load(f)
                self.config.update(user_config or {})
        
        self.save_config()
    
    def save_config(self):
        with open("config.yaml", "w") as f:
            yaml.dump(self.config, f)
    
    def __getitem__(self, key):
        return self.config.get(key)
    
    def __setitem__(self, key, value):
        self.config[key] = value
        self.save_config()
