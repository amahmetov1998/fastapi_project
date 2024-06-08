from fastapi import APIRouter, Depends, status
from pydantic import EmailStr
from starlette.responses import JSONResponse
from src.services.account_service import AccountService
from src.services.user_service import UserService
from src.auth.utils.auth_utils import get_current_user
from src.utils.unit_of_work import UnitOfWork
from fastapi import HTTPException
from src.schemas.user import UpdateUserSchema

router = APIRouter(prefix="/api/v1", tags=["Update user"])


@router.patch('/update-mail')
async def update_mail(new_email: EmailStr,
                      uow: UnitOfWork = Depends(UnitOfWork),
                      account: str = Depends(get_current_user)) -> JSONResponse:
    try:
        await AccountService().update_email(uow=uow,
                                            new_email=new_email,
                                            account=account)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="email already exists")

    return JSONResponse(content="changed successfully",
                        status_code=status.HTTP_200_OK)


@router.patch('/update-name')
async def update_name(user: UpdateUserSchema,
                      uow: UnitOfWork = Depends(UnitOfWork),
                      account: str = Depends(get_current_user)) -> JSONResponse:
    try:
        await UserService().update_name(uow=uow,
                                        first_name=user.first_name,
                                        last_name=user.last_name,
                                        account=account)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="mail not found")

    return JSONResponse(content="changed successfully",
                        status_code=status.HTTP_200_OK)
