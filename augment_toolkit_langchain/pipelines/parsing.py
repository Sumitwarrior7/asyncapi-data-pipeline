from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional

class Questions(BaseModel):
    q1: str = Field(description="First Generated question about the context")
    q2: str = Field(description="Second Generated question about the context")
    q3: str = Field(description="Third Generated question about the context")
    # context: str = Field(description="Summary of the context")

class Answer(BaseModel):
    text: str = Field(description="Answer to the question")
    question: str = Field(description="Original question being answered")

class Conversation(BaseModel):
    turns: List[dict] = Field(description="List of conversation turns")

class Conversation(BaseModel):
    turns: List[dict] = Field(description="List of conversation turns")

def get_qa_parser() -> PydanticOutputParser:
    return PydanticOutputParser(pydantic_object=Questions)

def get_answer_parser() -> JsonOutputParser:
    return JsonOutputParser(pydantic_object=Answer)

def get_conversation_parser() -> JsonOutputParser:
    return JsonOutputParser(pydantic_object=Conversation)
