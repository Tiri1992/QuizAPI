from fastapi import APIRouter

quiz_router = APIRouter(
    prefix="/quiz",
    tags=["QUIZ"],
)


@quiz_router.get("/")
def get_random_quiz():
    pass
