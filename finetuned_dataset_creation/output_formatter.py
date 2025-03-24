from utils import write_jsonl, write_json
from datetime import datetime
from typing import List, Dict

def save_dataset(conversations: List[Dict], config: dict):
    output_path = f"output/dataset_{datetime.now().strftime('%Y%m%d_%H%M')}.jsonl"
    write_jsonl(conversations, output_path)
    
    meta = {
        "created_at": datetime.now().isoformat(),
        "model": config["model_name"],
        "num_samples": len(conversations),
        "stats": {
            "avg_turns": sum(len(c["conversations"]) for c in conversations)/len(conversations)
        }
    }
    write_json(meta, "output/metadata.json")
