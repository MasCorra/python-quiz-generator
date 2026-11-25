from fastapi import APIRouter, HTTPException

from features.quiz import quiz_service
from src.features.quiz.quiz_models import PostGenerateQuizResponse, PostGenerateQuizRequest

quiz_router = APIRouter(
    prefix="/api/quizzes"
    )

@quiz_router.post("", response_model= PostGenerateQuizResponse)
def post_generate_quiz_endpoint(body: PostGenerateQuizRequest):
    quiz = quiz_service.generate_quiz(body.text)
    return {"quiz": quiz}
