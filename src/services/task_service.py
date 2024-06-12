from src.utils.unit_of_work import UnitOfWork


class TaskService:

    @classmethod
    async def add_task(cls, uow: UnitOfWork,
                       title: str,
                       description: str,
                       author_id: int,
                       responsible_id: int,
                       observers_id: list[int],
                       executors_id: list[int],
                       deadline: str,
                       status: str,
                       time_estimation: str) -> None:
        async with uow:

            task_id: int = await uow.task.add_one_and_get_id(title=title,
                                                             description=description,
                                                             deadline=deadline,
                                                             status=status,
                                                             time_estimation=time_estimation)
            await uow.user.update_one_by_id(_id=author_id, task_author_id=task_id)
            await uow.user.update_one_by_id(_id=responsible_id, task_responsible_id=task_id)
            for observer_id in observers_id:
                await uow.user.update_one_by_id(_id=observer_id, task_observer_id=task_id)
            for executor_id in executors_id:
                await uow.user.update_one_by_id(_id=executor_id, task_executor_id=task_id)

    @classmethod
    async def update_task_title(cls, uow: UnitOfWork, _id: int, new_name: str) -> None:
        async with uow:
            await uow.task.update_one_by_id(_id=_id, new_title=new_name)

    @classmethod
    async def delete_task(cls, uow: UnitOfWork, _id: int) -> None:
        async with uow:
            await uow.task.delete_by_query(id=_id)
