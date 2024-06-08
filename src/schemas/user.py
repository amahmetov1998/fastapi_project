from pydantic import BaseModel, EmailStr


class SignInSchema(BaseModel):
    mail: EmailStr
    password: str


class PasswordSchema(BaseModel):
    password: str


class UpdateUserSchema(BaseModel):
    first_name: str
    last_name: str


class AddUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
