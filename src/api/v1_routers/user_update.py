from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse

from src.schemas.account import AccountSchema
from src.services.account_service import AccountService
from src.services.user_service import UserService
from src.auth.utils.auth_utils import get_current_user
from src.utils.unit_of_work import UnitOfWork
from fastapi import HTTPException
from src.schemas.user import UpdateUserSchema

router = APIRouter(prefix="/api/v1", tags=["User update"])


@router.put('/update-mail')
async def update_mail(account: AccountSchema,
                      uow: UnitOfWork = Depends(UnitOfWork),
                      _id: int = Depends(get_current_user)) -> JSONResponse:
    try:
        await AccountService().update_email(uow=uow, new_email=account.email, _id=_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="changed successfully",
                        status_code=status.HTTP_200_OK)


@router.put('/update-name')
async def update_name(user: UpdateUserSchema,
                      uow: UnitOfWork = Depends(UnitOfWork),
                      _id: int = Depends(get_current_user)) -> JSONResponse:
    try:
        await UserService().update_name(uow=uow,
                                        first_name=user.first_name,
                                        last_name=user.last_name,
                                        _id=_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="changed successfully",
                        status_code=status.HTTP_200_OK)
