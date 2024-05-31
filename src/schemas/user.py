from pydantic import BaseModel


class UserSchema(BaseModel):
    mail: str
    password: str


class PasswordSchema(BaseModel):
    password: str


class ChangeUserSchema(BaseModel):
    first_name: str
    last_name: str

