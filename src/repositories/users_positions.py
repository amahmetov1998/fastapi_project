from sqlalchemy import update

from src.models import UserPosition
from src.utils.repository import SqlAlchemyRepository


class UsersPositionsRepository(SqlAlchemyRepository):
    model = UserPosition

    async def update_user_position_by_position_id(self, position_id, user_id):
        query = update(self.model).filter_by(position_id=position_id).values(user_id=user_id)
        await self.session.execute(query)
