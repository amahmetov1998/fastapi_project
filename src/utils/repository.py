from abc import ABC, abstractmethod

from sqlalchemy import insert, Result, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_id(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_by_query_one_or_none(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update_one_by_id(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_query(self, *args, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, **kwargs) -> None:
        query = insert(self.model).values(**kwargs)
        await self.session.execute(query)

    async def add_one_and_get_id(self, **kwargs) -> int:
        query = insert(self.model).values(**kwargs).returning(self.model.id)
        result: Result = await self.session.execute(query)
        return result.scalar_one()

    async def get_by_query_one_or_none(self, **kwargs) -> type(model) | None:
        query = select(self.model).filter_by(**kwargs)
        result: Result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_one_by_id(self, _id, **values) -> type(model) | None:
        query = update(self.model).filter(self.model.id == _id).values(**values).returning(self.model)
        _obj = await self.session.execute(query)
        return _obj.scalar_one_or_none()

    async def delete_by_query(self, **kwargs) -> None:
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)
