from config import Config
from utils import list_input_files, read_file
from text_processor import chunk_text, filter_chunks
from qa_generator import generate_questions, generate_answers, validate_qa
from conversation_generator import generate_conversation
from output_formatter import save_dataset
import time

def process_file(path: str, config: dict):
    print(f"Processing {path}")
    text = read_file(path)
    
    # Chunking
    chunks = chunk_text(text, config["chunk_size"])
    chunks = filter_chunks(chunks, config)
    
    # QA Generation
    qa_pairs = []
    for chunk in chunks:
        questions = generate_questions(chunk, config)
        answers = generate_answers(questions, config)
        qa_pairs.extend(validate_qa(answers, config))
    
    # Conversation Generation
    conversations = []
    for qa in qa_pairs:
        conv = generate_conversation(qa, config)
        if conv:
            conversations.append(conv)
    
    return conversations

def main():
    config = Config().config
    files = [f"input/{f}" for f in list_input_files()]
    
    if not files:
        print("No .txt files in input/ directory")
        return
    
    all_convs = []
    for file in files:
        all_convs.extend(process_file(file, config))
    
    save_dataset(all_convs, config)
    print(f"Generated {len(all_convs)} conversations in output/")

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Finished in {time.time()-start:.2f}s")
