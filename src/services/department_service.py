from sqlalchemy import text
from sqlalchemy_utils import Ltree

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
    async def delete_department(cls, uow: UnitOfWork, _id: int) -> None:
        async with uow:
            await uow.department.delete_by_query(id=_id)

    @classmethod
    async def update_department(cls, uow: UnitOfWork, _id: int, name: str) -> None:
        async with uow:
            await uow.department.update_one_by_id(_id=_id, name=name)

    @classmethod
    async def change_struct(cls, _id: int) -> None:

        # async with uow:
        #     node = await uow.department.get_by_query_one_or_none(id=_id)
        #
        #     parent = await uow.department.get_parent(node=node)
        #
        #     children: list = await uow.department.get_children(node=node)
        #     children.remove(node)
        #
        #     for child in children:
        #         child.path = parent.path + child.path[2:]
        #
        #     node.path = id_

        async with async_session_maker() as session:
            data = {'group_id_str': str(_id), 'group_id_int': _id}

            sql = text(
                """
                UPDATE public.struct_adm t
                SET path = nu.new_path
                FROM  (
                   WITH x AS (
                      SELECT *, index(path, :group_id_str) AS i
                      FROM   public.struct_adm
                      WHERE  path ~ '*.:group_id_int.*'
                      )
                   SELECT
                        *,
                        subpath(path, 0, i) || CASE WHEN nlevel(path) > i+1 THEN subpath(path, i+1) ELSE '' END AS new_path
                   FROM x
                   ) nu
                WHERE nu.id = t.id AND t.id <> :group_id_int;
                """,
            )
            await session.execute(sql, data)
            await session.commit()
