from sqlalchemy import update

from src.models import StructAdm
from src.utils.repository import SqlAlchemyRepository


class DepartmentRepository(SqlAlchemyRepository):
    model = StructAdm

    async def update_one_by_name(self, old_name, new_name) -> type(model) | None:
        query = update(self.model).filter(self.model.name == old_name).values(name=new_name)
        _obj = await self.session.execute(query)
        return _obj.scalar_one_or_none()
