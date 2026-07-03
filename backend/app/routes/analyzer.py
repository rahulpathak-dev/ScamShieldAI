from fastapi import APIRouter
from pydantic import BaseModel
from app.services.analyzer import ScamAnalyzer

router = APIRouter(prefix="/api/analyze", tags=["analysis"])
analyzer = ScamAnalyzer()


class AnalyzeRequest(BaseModel):
    message: str


@router.post("")
def analyze_message(payload: AnalyzeRequest) -> dict:
    return analyzer.analyze(payload.message)
