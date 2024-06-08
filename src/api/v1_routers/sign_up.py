from starlette import status
from fastapi import APIRouter, Depends, HTTPException

from src.auth.utils import token_service
from src.services.company_service import CompanyService
from src.services.account_service import AccountService
from fastapi.responses import JSONResponse
from src.auth.utils import email_service
from src.schemas.company import AddCompanySchema
from src.schemas.account import AccountSchema
from src.schemas.invite_token import TokenSchema
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/auth/api/v1", tags=["Sign up"])


@router.post('/check_account')
async def validate_email(account: AccountSchema, uow: UnitOfWork = Depends(UnitOfWork)) -> JSONResponse:
    try:
        token: int = token_service.create_token()
        await AccountService().check_email_and_add_token(uow=uow,
                                                         account=account.email,
                                                         invite_token=token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="mail already exists")

    await email_service.send_email(email=account.email, token=token)

    return JSONResponse(content="please, check email",
                        status_code=status.HTTP_200_OK)


@router.post('/sign-up')
async def validate_code(code: TokenSchema, uow: UnitOfWork = Depends(UnitOfWork)) -> JSONResponse:
    try:
        await AccountService().create_account(invite_token=code.invite_token, uow=uow)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='invalid code')

    return JSONResponse(content='created successfully',
                        status_code=status.HTTP_201_CREATED)


@router.post('/sign-up-complete')
async def create_company(new_info: AddCompanySchema, uow: UnitOfWork = Depends(UnitOfWork)) -> JSONResponse:
    try:
        await CompanyService().add_company(uow=uow,
                                           account=new_info.account,
                                           password=new_info.password,
                                           first_name=new_info.first_name,
                                           last_name=new_info.last_name,
                                           company_name=new_info.company_name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='invalid data')

    return JSONResponse(content='created successfully',
                        status_code=status.HTTP_201_CREATED)
