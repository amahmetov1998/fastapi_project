from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from starlette.responses import JSONResponse

from src.auth.utils import JWT_service
from src.schemas.token import TokenInfo
from src.schemas.user import PasswordSchema
from src.auth.utils import email_service
from src.services.user_service import UserService
from src.auth.utils.auth_utils import get_current_user, get_current_mail
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/create/api/v1", tags=["User"])


@router.post('/create-user', response_model=TokenInfo)
async def create_user(account: str = Depends(get_current_user), uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        email: str = await UserService().create_user(uow=uow, account=account)
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='do not have rights')

    await email_service.send_email_with_token(email)

    jwt_payload: dict = {
                "email": email
            }
    token: str = JWT_service.encode_jwt(payload=jwt_payload)

    return TokenInfo(access_token=token, token_type="Bearer")


@router.post('/verification')
async def verify_email(data: PasswordSchema, uow: UnitOfWork = Depends(UnitOfWork),
                       account: EmailStr = Depends(get_current_mail)):

    try:
        await UserService().confirm_auth(uow=uow, account=account, password=data.password)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='mail not found')

    return JSONResponse(content='created successfully',
                        status_code=status.HTTP_201_CREATED)
