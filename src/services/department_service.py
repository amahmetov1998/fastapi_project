from src.models import StructAdm
from src.models.struct_adm import id_seq
from src.database.db import async_engine, async_session_maker
from src.utils.unit_of_work import UnitOfWork


class DepartmentService:

    @classmethod
    async def add_department(cls, department_name: str) -> None:
        async with async_engine.begin() as conn:
            _id = await conn.execute(id_seq)
        async with async_session_maker() as session:
            new = StructAdm(_id=_id, name=department_name, parent=None)
            session.add(new)
            await session.commit()

    @classmethod
    async def delete_department(cls, uow: UnitOfWork, department_name: str) -> None:
        async with uow:
            await uow.department.delete_by_query(name=department_name)
