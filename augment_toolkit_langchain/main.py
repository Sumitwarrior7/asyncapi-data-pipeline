from pipelines.chunking import chunk_document
from pipelines.generation import qa_generation_chain, answer_generation_chain
from pipelines.parsing import get_conversation_parser
from utils import load_documents, save_output
import json
from dotenv import load_dotenv

load_dotenv()

def process_chunk(chunk: str):
    """Process a single text chunk through the pipeline"""
    # print(1)
    qa_chain = qa_generation_chain()
    # print(2)
    answer_chain = answer_generation_chain()
    # print(3)
    conv_parser = get_conversation_parser()
    # print(4)
    
    try:
        # Generate questions
        print("chunk :", chunk)
        print()
        qa_result = qa_chain.invoke({"input": chunk})
        print("qa resp :", qa_result)
        if not qa_result or "questions" not in qa_result:
            return []
        
        conversations = []
        for question in qa_result["questions"]:
            # Generate answer
            answer_result = answer_chain.invoke({
                "input": f"Context: {chunk}\nQuestion: {question['text']}"
            })
            
            # Build conversation
            conversation = {
                "turns": [
                    {"from": "human", "value": question['text']},
                    {"from": "gpt", "value": answer_result['text']}
                ]
            }
            
            # Validate conversation structure
            parsed = conv_parser.parse(json.dumps(conversation))
            conversations.append(parsed)
        
        return conversations
    
    except Exception as e:
        print(f"Error processing chunk: {e}")
        return []

def main():
    documents = load_documents()
    all_conversations = []
    # print("docs :", documents)
    
    for doc in documents:
        chunks = chunk_document(doc)
        # print("chunks :", chunks)
        for chunk in chunks:
            all_conversations.extend(process_chunk(chunk))
    
    
    save_output(all_conversations)
    print(f"Generated {len(all_conversations)} valid conversations")

if __name__ == "__main__":
    main()
