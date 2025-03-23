from transformers import AutoTokenizer, AutoModel
import torch
import json
import os
from peft import get_peft_model, LoraConfig, TaskType
from transformers import AutoModelForCausalLM, TrainingArguments, Trainer
import os
from dotenv import load_dotenv
# from datasets import Dataset

load_dotenv()

# Load LLaMA tokenizer
LLAMA3_MODEL_NAME = "meta-llama/Llama-3.1-8B"
MISTRAL_MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"

READ_AUTH_TOKEN = os.getenv("READ_AUTH_TOKEN")
tokenizer = AutoTokenizer.from_pretrained(LLAMA3_MODEL_NAME)

# Function to tokenize entire dictionary
def tokenize_data(data):
    text_data = json.dumps(data, separators=(',', ':'))  # Convert dict to JSON string
    tokens = tokenizer(text_data, padding="max_length", truncation=True, return_tensors="pt")
    return tokens

# Function to convert tokens to vectors
def tokenize_and_vectorize(data_list):
    model = AutoModel.from_pretrained(LLAMA3_MODEL_NAME)
    model.eval()

    vectorized_data = []
    for data in data_list:
        tokens = tokenize_data(data)
        with torch.no_grad():
            embeddings = model(**tokens).last_hidden_state.mean(dim=1)  # Get sentence embeddings
        vectorized_data.append(embeddings)
    
    return vectorized_data

# Fine-tuning setup (LoRA or QLoRA)
def fine_tune_llm(dataset):
    model = AutoModelForCausalLM.from_pretrained(
        LLAMA3_MODEL_NAME,
        load_in_4bit=True  # Use QLoRA for low VRAM usage
    )
    
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,  # Rank
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none"
    )
    
    model = get_peft_model(model, lora_config)

    training_args = TrainingArguments(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        save_steps=100,
        output_dir="./fine_tuned_llama",
        evaluation_strategy="epoch",
        learning_rate=2e-4,
        num_train_epochs=3,
        fp16=True
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset
    )

    trainer.train()

# Example dataset preprocessing
data = [
    {
        "_id": {"$oid": "1"},
        "repo_name": "spec",
        "file_name": "RELEASE_PROCESS.md",
        "file_extension": ".md",
        "file_path": "RELEASE_PROCESS.md",
        "depth_rank": {"$numberInt": "0"},
        "content": "Feel free to use other communication channels..."
    },
    {
        "_id": {"$oid": "2"},
        "repo_name": "spec",
        "file_name": "readme.md",
        "file_extension": ".md",
        "file_path": "readme.md",
        "depth_rank": {"$numberInt": "0"},
        "content": "I am coming home..."
    },
]

# Tokenize and vectorize the dataset
vectorized_data = tokenize_and_vectorize(data)
print("vector :", vectorized_data)

# Convert to Hugging Face dataset format for fine-tuning
# dataset = Dataset.from_dict({"input_ids": [vec.numpy() for vec in vectorized_data]})

# Fine-tune LLaMA
# fine_tune_llm(dataset)
