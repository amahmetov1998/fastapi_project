from sqlalchemy import select, Result

from src.models import Position, User, StructAdm, UserPosition
from src.utils.unit_of_work import UnitOfWork
from src.models.struct_adm import id_seq
from src.database.db import async_engine, async_session_maker


class AssignService:

    @classmethod
    async def assign_leader(cls, uow: UnitOfWork, department_id: int, position_id: int, user_id: int) -> None:
        async with uow:
            position: None | Position = await uow.position.get_by_query_one_or_none(id=position_id)
            user: None | User = await uow.user.get_by_query_one_or_none(id=user_id)

            user_position_id: int = await uow.user_position.add_one_and_get_id(user_id=user.id,
                                                                               position_id=position.id)

        async with async_engine.begin() as conn:
            _id = await conn.execute(id_seq)
        async with async_session_maker() as session:
            query = select(StructAdm).filter_by(id=department_id)
            result: Result = await session.execute(query)
            department: None | StructAdm = result.scalar_one_or_none()

            new = StructAdm(_id=_id, user_position_id=user_position_id, parent=department)
            session.add(new)
            await session.commit()

    @classmethod
    async def reassign_user(cls, uow: UnitOfWork, position_id: int, user_id: int) -> None:
        async with uow:
            position: None | Position = await uow.position.get_by_query_one_or_none(id=position_id)
            user: None | User = await uow.user.get_by_query_one_or_none(id=user_id)

            await uow.user_position.update_user_position_by_position_id(position_id=position.id, user_id=user.id)

    @classmethod
    async def assign_user(cls, uow: UnitOfWork, leader_position_id: int, position_id: int,
                          user_id: int) -> None:
        async with uow:
            position: None | Position = await uow.position.get_by_query_one_or_none(id=position_id)
            user: None | User = await uow.user.get_by_query_one_or_none(id=user_id)

            user_position_id: int = await uow.user_position.add_one_and_get_id(user_id=user.id,
                                                                               position_id=position.id)

        async with async_engine.begin() as conn:
            _id = await conn.execute(id_seq)
        async with async_session_maker() as session:
            query = select(Position).filter_by(id=leader_position_id)
            result: Result = await session.execute(query)
            position: None | Position = result.scalar_one_or_none()

            query = select(UserPosition).filter_by(position_id=position.id)
            result: Result = await session.execute(query)
            user_position: None | UserPosition = result.scalar_one_or_none()

            query = select(StructAdm).filter_by(user_position_id=user_position.id)
            result: Result = await session.execute(query)
            leader: None | StructAdm = result.scalar_one_or_none()

            new = StructAdm(_id=_id, user_position_id=user_position_id, parent=leader)
            session.add(new)
            await session.commit()
