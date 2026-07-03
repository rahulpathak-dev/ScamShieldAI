from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.nlp_dto import ModelInfoDTO, ScamPredictionRequest, ScamPredictionResponse
from app.application.services.nlp_prediction_service import ScamPredictionService
from app.core.config import Settings, get_settings

router = APIRouter(prefix="/ml", tags=["ml"])


def get_prediction_service(settings: Annotated[Settings, Depends(get_settings)]) -> ScamPredictionService:
    return ScamPredictionService(settings)


@router.post("/predict", response_model=ScamPredictionResponse, summary="Predict whether text is scam or safe")
def predict_scam(
    payload: ScamPredictionRequest,
    service: Annotated[ScamPredictionService, Depends(get_prediction_service)],
) -> ScamPredictionResponse:
    return service.predict(payload.text)


@router.get("/model", response_model=ModelInfoDTO, summary="Get active scam classifier model metadata")
def model_info(service: Annotated[ScamPredictionService, Depends(get_prediction_service)]) -> ModelInfoDTO:
    return service.model_info()