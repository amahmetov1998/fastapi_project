from fastapi import Depends, HTTPException
from pydantic import EmailStr
from starlette import status

from src.services.account_service import AccountService
from src.services.user_service import UserService
from src.utils.unit_of_work import UnitOfWork
from src.auth.utils.JWT_service import get_data_from_token_payload
from src.schemas.user import UserSchema
from src.models.account import Account


async def check_account(account: EmailStr, uow: UnitOfWork = Depends(UnitOfWork)) -> None | EmailStr:
    _obj: None | Account = await AccountService().check_email(uow=uow, account=account)
    if _obj:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="mail already exists")
    return account


async def get_current_mail(payload: dict = Depends(get_data_from_token_payload)) -> str:
    email: str = payload.get("email")
    return email


async def get_current_user(payload: dict = Depends(get_data_from_token_payload), uow: UnitOfWork = Depends(UnitOfWork)) -> str:
    email: str = payload.get("email")
    _obj: None | Account = await AccountService().check_email(uow=uow, account=email)
    if not _obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='user not found')
    return email


async def validate_auth_user(user: UserSchema, uow: UnitOfWork = Depends(UnitOfWork)) -> UserSchema:
    try:
        await UserService().check_user(uow=uow,
                                       account=user.mail,
                                       password=user.password)
        return user

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='invalid mail or password')
