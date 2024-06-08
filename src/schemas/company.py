from pydantic import BaseModel, EmailStr


class AddCompanySchema(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str
