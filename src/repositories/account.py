from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.models import Account
from src.utils.repository import SqlAlchemyRepository


class AccountRepository(SqlAlchemyRepository):
    model = Account

    async def get_account_by_query(self, mail) -> Account | None:
        query = select(self.model).filter_by(mail=mail).options(joinedload(self.model.user))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
