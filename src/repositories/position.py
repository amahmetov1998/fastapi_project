from sqlalchemy import update

from src.models import Position
from src.utils.repository import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = Position

    async def update_position_name(self, old_name, new_name):
        query = update(self.model).filter_by(name=old_name).values(name=new_name)
        await self.session.execute(query)
