__all__ = [
    'user_router',
    'company_router',
    'authorization_router',
    'authentication_router',
    'user_router'
]

from src.api.v1_routers.company import router as company_router
from src.api.v1_routers.authorization import router as authorization_router
from src.api.v1_routers.authentication import router as authentication_router
from src.api.v1_routers.user import router as user_router
