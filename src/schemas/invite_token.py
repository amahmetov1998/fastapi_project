from pydantic import BaseModel


class TokenSchema(BaseModel):
    invite_token: int
