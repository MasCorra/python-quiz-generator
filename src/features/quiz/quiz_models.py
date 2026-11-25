from pydantic import BaseModel, Field
from typing import Literal

class PostGenerateQuizRequest(BaseModel):
    text: str

class PostGenerateQuizResponse(BaseModel):
    quiz : Quiz

class Question(BaseModel):
    id_question: int
    question : str
    options : Options
    correct_answer : Literal["a", "b", "c", "d"]

class Options(BaseModel):
    a: str
    b: str
    c: str
    d: str

class Quiz(BaseModel):
    questions: list[Question] = Field(min_length=10, max_length=10)

