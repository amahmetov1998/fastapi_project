from src.models import StructAdm
from src.utils.unit_of_work import UnitOfWork


class PositionService:

    @classmethod
    async def add_position(cls, uow: UnitOfWork, department_name: str, position_name: str) -> None:
        async with uow:
            position_id: int = await uow.position.add_one_and_get_id(name=position_name)
            department: None | StructAdm = await uow.department.get_by_query_one_or_none(name=department_name)
            await uow.struct_position.add_one(struct_adm_id=department.id, position_id=position_id)

    @classmethod
    async def update_position(cls, uow: UnitOfWork, _id: int, new_position_name: str) -> None:
        async with uow:
            await uow.position.update_one_by_id(_id=_id, name=new_position_name)

    @classmethod
    async def delete_position(cls, uow: UnitOfWork, _id: int) -> None:
        async with uow:
            await uow.position.delete_by_query(id=_id)
