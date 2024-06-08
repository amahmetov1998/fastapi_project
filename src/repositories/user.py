from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from src.models import User
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User

    async def get_user_by_query_one_or_none(self, _id):
        query = select(self.model).filter_by(id=_id).options(joinedload(self.model.company))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_name(self, _id, first_name, last_name):
        query = update(self.model).filter_by(id=_id).values(first_name=first_name, last_name=last_name)
        await self.session.execute(query)
