from pydantic import EmailStr

from src.models import Account
from src.auth.utils import password_service
from src.utils.unit_of_work import UnitOfWork


class CompanyService:

    @classmethod
    async def add_company(cls, uow: UnitOfWork, account: EmailStr, password: str, first_name: str, last_name: str,
                          company_name: str) -> None:
        async with uow:
            company_id: int = await uow.company.add_one_and_get_id(company_name=company_name)
            account: Account | None = await uow.account.get_by_query_one_or_none(mail=account)
            user_id: int = await uow.user.add_one_and_get_id(is_admin=True,
                                                             first_name=first_name,
                                                             last_name=last_name)
            await uow.members.add_one(user_id=user_id,
                                      company_id=company_id)

            await uow.secrets.add_one(account_id=account.id,
                                      user_id=user_id,
                                      password=password_service.hash_password(password))
