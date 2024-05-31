from fastapi import APIRouter, Depends
from src.auth.utils import JWT_service
from src.auth.utils.auth_utils import validate_auth_user
from src.schemas.user import UserSchema
from src.schemas.token import TokenInfo


router = APIRouter(prefix="/authenticate/api/v1", tags=["Authentication"])


@router.post('/login', response_model=TokenInfo)
async def login_user(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload: dict = {
        "email": user.mail
    }
    token: str = JWT_service.encode_jwt(payload=jwt_payload)

    return TokenInfo(access_token=token, token_type="Bearer")
