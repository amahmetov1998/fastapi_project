from sqlalchemy import update

from src.models import Task

from src.utils.repository import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository):
    model = Task

    async def update_one_by_title(self, old_title, new_title) -> None:
        query = update(self.model).filter(self.model.title == old_title).values(title=new_title)
        _obj = await self.session.execute(query)
