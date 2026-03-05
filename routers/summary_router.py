from fastapi import APIRouter
from services.summarizer_service import summarize_text

router = APIRouter()

@router.post("/summary")
def summary(text: str):

    result = summarize_text(text)

    return {"summary": result}