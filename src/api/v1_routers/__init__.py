__all__ = [
    'user_router',
    'company_router',
    'authorization_router',
    'authentication_router',
    'user_router',
    'department_router',
    'position_router',
    'assign_router',
    'task_router'
]

from src.api.v1_routers.sign_up import router as company_router
from src.api.v1_routers.update_user import router as authorization_router
from src.api.v1_routers.sign_in import router as authentication_router
from src.api.v1_routers.new_user import router as user_router
from src.api.v1_routers.department import router as department_router
from src.api.v1_routers.position import router as position_router
from src.api.v1_routers.assign_users import router as assign_router
from src.api.v1_routers.tasks import router as task_router
