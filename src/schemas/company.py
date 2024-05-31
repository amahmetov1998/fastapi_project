from pydantic import BaseModel


class CreateCompanySchema(BaseModel):
    password: str
    first_name: str
    last_name: str
    company_name: str
