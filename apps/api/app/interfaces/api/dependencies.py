from functools import lru_cache

from app.application.services.multilingual_service import MultilingualService
from app.application.services.notification_service import NotificationService
from app.application.services.platform_analysis_service import PlatformAnalysisService
from app.application.use_cases.analyze_text_message import AnalyzeTextMessageUseCase
from app.core.config import get_settings
from app.domain.services.risk_engine import ScamRiskEngine
from app.infrastructure.persistence.postgres_analysis_repository import ResilientAnalysisRepository


@lru_cache
def get_analysis_repository() -> ResilientAnalysisRepository:
    return ResilientAnalysisRepository()


def get_analyze_text_use_case() -> AnalyzeTextMessageUseCase:
    return AnalyzeTextMessageUseCase(
        risk_engine=ScamRiskEngine(),
        repository=get_analysis_repository(),
    )


def get_notification_service() -> NotificationService:
    return NotificationService(settings=get_settings())

@lru_cache
def get_multilingual_service() -> MultilingualService:
    return MultilingualService()


def get_platform_analysis_service() -> PlatformAnalysisService:
    return PlatformAnalysisService(
        analyze_use_case=get_analyze_text_use_case(),
        multilingual_service=get_multilingual_service(),
    )