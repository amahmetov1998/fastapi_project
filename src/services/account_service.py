from pydantic import EmailStr

from src.models import Account
from src.utils.unit_of_work import UnitOfWork
from src.models import Invite


class AccountService:

    @classmethod
    async def check_email_and_add_token(cls, uow: UnitOfWork, account: EmailStr, invite_token: int) -> None:
        async with uow:
            await uow.account.get_by_query_one_or_none(mail=account)
            await uow.invite.add_one(token=invite_token, temp_mail=account)

    @classmethod
    async def create_account(cls, uow: UnitOfWork, invite_token: int):
        async with uow:
            invite: Invite | None = await uow.invite.get_by_query_one_or_none(token=invite_token)
            mail_id: int = await uow.account.add_one_and_get_id(mail=invite.temp_mail)
            invite.account_id = mail_id

    @classmethod
    async def check_email(cls, uow: UnitOfWork, account: EmailStr) -> Account | None:
        async with uow:
            _obj: Account | None = await uow.account.get_by_query_one_or_none(mail=account)
            return _obj

    @classmethod
    async def check_admin_user(cls, uow: UnitOfWork, account: EmailStr) -> None:
        async with uow:
            admin_account: Account | None = await uow.account.get_account_by_query(
                mail=account
            )
            if not (admin_account and admin_account.user.is_admin):
                raise

    @classmethod
    async def update_email(cls, uow: UnitOfWork, new_email: EmailStr, account: str) -> None:
        async with uow:
            exists: Account | None = await uow.account.get_by_query_one_or_none(mail=new_email)
            if exists:
                raise

            await uow.account.update_mail(new_email=new_email,
                                          old_email=account)
