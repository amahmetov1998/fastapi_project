from sqlalchemy import select

from src.models import StructAdm
from src.utils.repository import SqlAlchemyRepository


class DepartmentRepository(SqlAlchemyRepository):
    model = StructAdm

    async def get_parent(self, node):
        query = select(self.model).filter(self.model.path.ancestor_of(node.path))
        result = await self.session.execute(query)
        return result.scalar()

    async def get_children(self, node):
        query = select(self.model).filter(self.model.path.descendant_of(node.path))
        result = await self.session.execute(query)
        return result.scalars().all()
