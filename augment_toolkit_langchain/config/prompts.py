chunking:
  splitter: "recursive"
  chunk_size: 1500
  chunk_overlap: 200

ollama:
  model: "gemma3:4b"
  temperature: 0.5
  max_tokens: 1024

qa_generation:
  system_prompt: |
    Generate questions and answers from the provided context. 
    Follow exactly these rules:
    1. Questions must be answerable from the context
    2. Answers must contain actual information
    3. Use clear and concise language

output_format:
  schema:
    - name: "conversation"
      type: "list"
      description: "List of conversation turns"
      fields:
        - name: "from"
          type: "string"
          enum: ["human", "gpt"]
        - name: "value"
          type: "string"
