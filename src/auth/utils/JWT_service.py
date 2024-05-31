from datetime import timedelta, datetime
import jwt
from src.config import settings
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

http_bearer = HTTPBearer()


def encode_jwt(payload: dict,
               private_key: str = settings.auth_jwt.private_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm,
               expire_minutes: int = settings.auth_jwt.access_token_expires_in) -> str:
    payload = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    payload.update(exp=expire)
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(token: str | bytes,
               public_key: str = settings.auth_jwt.public_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm) -> dict:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def get_data_from_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> dict:
    token = credentials.credentials

    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="invalid token")

    return payload
