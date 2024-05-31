__all__ = [
    'router'
]

from fastapi import APIRouter
from src.api.v1_routers import (
    company_router, user_router, authentication_router, authorization_router
)

router = APIRouter()

router.include_router(company_router)
router.include_router(authentication_router)
router.include_router(authorization_router)
router.include_router(user_router)
