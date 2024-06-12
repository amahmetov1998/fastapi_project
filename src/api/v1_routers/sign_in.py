from fastapi import APIRouter, Depends
from src.auth.utils import JWT_service
from src.auth.utils.auth_utils import validate_auth_user
from src.schemas.user import SignInSchema
from src.schemas.jwt_token import TokenInfo


router = APIRouter(prefix="/api/v1", tags=["Sign in"])


@router.post('/sign-in', response_model=TokenInfo)
async def sign_in(user: SignInSchema = Depends(validate_auth_user)):
    jwt_payload: dict = {
        "email": user.mail,
        "id": user.id
    }
    token: str = JWT_service.encode_jwt(payload=jwt_payload)

    return TokenInfo(access_token=token, token_type="Bearer")
