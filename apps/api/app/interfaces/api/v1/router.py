from fastapi import APIRouter

from app.interfaces.api.v1.analysis import router as analysis_router
from app.interfaces.api.v1.assistant import router as assistant_router
from app.interfaces.api.v1.auth import router as auth_router
from app.interfaces.api.v1.voice import router as voice_router
from app.interfaces.api.v1.mobile import router as mobile_router
from app.interfaces.api.v1.i18n import router as i18n_router
from app.interfaces.api.v1.enterprise import router as enterprise_router
from app.interfaces.api.v1.browser_extension import router as browser_extension_router
from app.interfaces.api.v1.ml import router as ml_router
from app.interfaces.api.v1.notifications import router as notifications_router
from app.interfaces.api.v1.persuasion import router as persuasion_router
from app.interfaces.api.v1.risk import router as risk_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(analysis_router)
router.include_router(ml_router)
router.include_router(persuasion_router)
router.include_router(risk_router)
router.include_router(notifications_router)
router.include_router(enterprise_router)
router.include_router(voice_router)
router.include_router(mobile_router)
router.include_router(browser_extension_router)
router.include_router(i18n_router)
router.include_router(assistant_router)