from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from src.services.company_service import CompanyService
from src.auth.utils import email_service, JWT_service
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from src.auth.utils.auth_utils import get_current_mail, check_account
from src.schemas.company import CreateCompanySchema
from src.schemas.token import TokenInfo
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/auth/api/v1", tags=["Company"])


@router.get('/check_account', response_model=TokenInfo)
async def validate_email(account: EmailStr = Depends(check_account)):

    await email_service.send_email_with_code(account)

    jwt_payload: dict = {
                "email": account
            }
    token: str = JWT_service.encode_jwt(payload=jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


@router.post('/sign-up')
async def validate_code(code: int, account: EmailStr = Depends(get_current_mail)):
    if code != email_service.VERIFICATION_CODE:
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                             detail=email_service.VERIFICATION_CODE)
    return account
    # return RedirectResponse(url='/auth/api/v1/sign-up-complete')


@router.post('/sign-up-complete')
async def create_company(new_info: CreateCompanySchema,
                         uow: UnitOfWork = Depends(UnitOfWork),
                         account: EmailStr = Depends(validate_code)) -> JSONResponse:
    try:
        await CompanyService().create_company(uow=uow, account=account, **new_info.model_dump())
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='company already exists')

    return JSONResponse(content='created successfully',
                        status_code=status.HTTP_201_CREATED)
