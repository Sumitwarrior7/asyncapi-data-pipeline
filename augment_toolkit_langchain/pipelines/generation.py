from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from parsing import get_qa_parser, get_answer_parser
import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

# def create_llm_chain(system_prompt: str, parser):
#     """Create a configured LLM chain with validation"""


#     model = ChatOllama(
#         model=os.getenv("OLLAMA_MODEL"),
#         temperature=float(os.getenv("TEMPERATURE")),
#         # other params...
#     )
    
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", system_prompt),
#         ("human", "{input}")
#     ])

#     prompt = PromptTemplate(
#         template="""
#             Please summarize the research paper titled "{paper_input}" with the following specifications:
#             Explanation Style: {style_input}
#             Explanation Length: {length_input}

#             Mathematical Details:

#             Include relevant mathematical equations if present in the paper.

#             Explain the mathematical concepts using simple, intuitive code snippets where applicable.

#             Analogies:

#             Use relatable analogies to simplify complex ideas.

#             If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.
#             Ensure the summary is clear, accurate, and aligned with the provided style and length.
#         """,
#         input_variables=['paper_input', 'style_input', 'length_input']
#     )

#     parser = get_qa_parser()
    
#     return prompt | model | parser

def qa_generation_chain():
    model = ChatOllama(
        model=os.getenv("SMALL_MODEL_NAME"),
        temperature=float(os.getenv("TEMPERATURE")),
        # other params...
    )

    parser = get_qa_parser()

    prompt = PromptTemplate(
        template="""
            Generate 3 questions from the context. Follow the format strictly.
            {format_instructions}
            Context: {context}
        """,
        input_variables=['context'],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )

    return prompt | model | parser

def answer_generation_chain():
    model = ChatOllama(
        model=os.getenv("SMALL_MODEL_NAME", "gemma3:1b"),
        temperature=float(os.getenv("TEMPERATURE", 0.5)),
        # other params...
    )

    parser = get_answer_parser()

    prompt = PromptTemplate(
        template="""
            Answer the question based on the context. Follow the format exactly..
            {format_instructions}
            Question: {question}
        """,
        input_variables=['question'],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )

    return prompt | model | parser


resp = qa_generation_chain().invoke({"context": "My name is sumit"})
print(resp)