from pydantic import EmailStr

from src.models import Account
from src.utils.unit_of_work import UnitOfWork


class AccountService:

    @classmethod
    async def check_email(cls, uow: UnitOfWork, account: EmailStr) -> Account | None:
        async with uow:
            _obj: Account | None = await uow.account.get_by_query_one_or_none(mail=account)
            return _obj

    @classmethod
    async def update_email(cls, uow: UnitOfWork, new_email: EmailStr, account: str) -> None:
        async with uow:
            exists: Account | None = await uow.account.get_by_query_one_or_none(mail=new_email)
            if exists:
                raise

            await uow.account.update_mail(new_email=new_email,
                                          old_email=account)
