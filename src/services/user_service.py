from pydantic import EmailStr

from src.models import Invite, Secrets, Account
from src.auth.utils import password_service
from src.utils.unit_of_work import UnitOfWork
from src.auth.utils.password_service import validate_password


class UserService:

    @classmethod
    async def check_user(cls, uow: UnitOfWork, account: str, password: str) -> None:
        async with uow:
            account: Account | None = await uow.account.get_account_by_query(
                mail=account
                )

            credentials: Secrets | None = await uow.secrets.get_by_query_one_or_none(
                    user_id=account.user.id
                )
            if not validate_password(password, credentials.password):
                raise

    @classmethod
    async def add_user(cls, uow: UnitOfWork, admin_account: str, first_name: str,
                       last_name: str, email: EmailStr, invite_token: int) -> str:
        async with uow:
            admin_account: Account | None = await uow.account.get_account_by_query(
                mail=admin_account
            )
            admin = await uow.user.get_user_by_query_one_or_none(_id=admin_account.user.id)

            user_id = await uow.user.add_one_and_get_id(is_admin=False,
                                                        first_name=first_name,
                                                        last_name=last_name)

            await uow.invite.add_one(token=invite_token, temp_mail=email)
            company = await uow.company.get_by_query_one_or_none(company_name=admin.company.company_name)

            account_id = await uow.account.add_one_and_get_id(mail=email)

            await uow.members.add_one(user_id=user_id,
                                      company_id=company.id)

            await uow.secrets.add_one(account_id=account_id,
                                      user_id=user_id)
            return email

    @classmethod
    async def set_password(cls, uow: UnitOfWork, invite_token: int, password: str) -> None:
        async with uow:
            invite: Invite | None = await uow.invite.get_by_query_one_or_none(token=invite_token)
            new_account: Account = await uow.account.get_account_by_query(mail=invite.temp_mail)
            invite.account_id = new_account.id
            await uow.secrets.update_secrets_by_id(_id=new_account.id,
                                                   password=password_service.hash_password(password))

    @classmethod
    async def update_name(cls, uow: UnitOfWork, first_name: str, last_name: str, account: str) -> None:
        async with uow:
            account: Account | None = await uow.account.get_account_by_query(mail=account)
            if not account:
                raise

            await uow.user.update_name(_id=account.user.id, first_name=first_name, last_name=last_name)
