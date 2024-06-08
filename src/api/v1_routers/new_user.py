from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from src.auth.utils import token_service
from src.schemas.invite_token import TokenSchema
from src.schemas.user import PasswordSchema, AddUserSchema
from src.auth.utils import email_service
from src.services.user_service import UserService
from src.auth.utils.auth_utils import get_current_auth_user
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/v1", tags=["Create user"])


@router.post('/add-user')
async def add_user(new_user: AddUserSchema,
                   account: str = Depends(get_current_auth_user),
                   uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        token: int = token_service.create_token()
        email: str = await UserService().add_user(uow=uow,
                                                  admin_account=account,
                                                  first_name=new_user.first_name,
                                                  last_name=new_user.last_name,
                                                  email=new_user.email,
                                                  invite_token=token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="mail already exists")

    await email_service.send_email(email=email, token=token)

    return JSONResponse(content="please, check email",
                        status_code=status.HTTP_200_OK)


@router.post('/add-user-complete')
async def set_password(code: TokenSchema, data: PasswordSchema, uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        await UserService().set_password(uow=uow, invite_token=code.invite_token, password=data.password)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid code")

    return JSONResponse(content="created successfully",
                        status_code=status.HTTP_201_CREATED)
