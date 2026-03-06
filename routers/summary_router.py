from fastapi import APIRouter
from services.summarizer_service import SummarizerService

router = APIRouter()

summarizer = SummarizerService()


@router.post("/summary")
def summary(text: str, model: str = "t5"):

    result = summarizer.summarize(text, model)

    return {
        "model": model,
        "summary": result
    }