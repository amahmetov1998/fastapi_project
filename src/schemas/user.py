from pydantic import BaseModel, EmailStr


class SignInSchema(BaseModel):
    mail: EmailStr
    password: str
    id: int | None = None


class PasswordSchema(BaseModel):
    password: str


class UpdateUserSchema(BaseModel):
    first_name: str
    last_name: str


class UpdateUserMailSchema(BaseModel):
    _id: int
    mail: str


class AddUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
