from sqlalchemy import select, Result, delete

from src.models import UserPosition, StructAdm, StructAdmPositions
from src.models.struct_adm import id_seq
from src.database.db import async_engine, async_session_maker


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
    async def delete_department(cls, department_name: str) -> None:
        async with async_session_maker() as session:
            query = select(StructAdm).filter_by(name=department_name)
            result: Result = await session.execute(query)
            department: None | StructAdm = result.scalar_one_or_none()

            query = delete(StructAdmPositions).filter_by(struct_adm_id=department.id)
            await session.execute(query)

            subtree = select(StructAdm).filter(StructAdm.path.descendant_of(department.path))
            result: Result = await session.execute(subtree)
            for _obj in result:
                query_1 = delete(StructAdm).filter_by(user_position_id=_obj[0].user_position_id)
                query_2 = delete(UserPosition).filter_by(id=_obj[0].user_position_id)
                await session.execute(query_1)
                await session.execute(query_2)
            await session.commit()
