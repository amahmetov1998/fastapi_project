from pydantic import EmailStr
from src.auth.utils import password_service
from src.utils.unit_of_work import UnitOfWork


class CompanyService:

    @classmethod
    async def create_company(cls, uow: UnitOfWork, account: EmailStr, **kwargs) -> None:
        async with uow:
            company_id: int = await uow.company.add_one_and_get_id(company_name=kwargs["company_name"])
            account_id: int = await uow.account.add_one_and_get_id(mail=account)
            user_id: int = await uow.user.add_one_and_get_id(is_admin=True,
                                                             first_name=kwargs["first_name"],
                                                             last_name=kwargs["last_name"]
                                                             )
            await uow.members.add_one(user_id=user_id,
                                      company_id=company_id
                                      )
            await uow.secrets.add_one(account_id=account_id,
                                      user_id=user_id,
                                      password=password_service.hash_password(kwargs["password"])
                                      )
