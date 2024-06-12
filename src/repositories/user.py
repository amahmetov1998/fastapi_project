from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.models import User
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User

    async def get_user_by_id(self, _id):
        query = select(self.model).filter_by(id=_id).options(joinedload(self.model.company))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
