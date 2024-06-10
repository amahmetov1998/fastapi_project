from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from src.schemas.task import AddTaskSchema, UpdateTaskNameSchema, DeleteTaskSchema
from src.services.task_service import TaskService
from src.auth.utils.auth_utils import get_current_auth_user
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/v1", tags=["Create task"], dependencies=[Depends(get_current_auth_user)])


@router.post('/add-task')
async def add_task(new_task: AddTaskSchema,
                   uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        await TaskService().add_task(uow=uow,
                                     title=new_task.title,
                                     description=new_task.description,
                                     author_id=new_task.author_id,
                                     responsible_id=new_task.responsible_id,
                                     observers_id=new_task.observers_id,
                                     executors_id=new_task.executors_id,
                                     deadline=new_task.deadline,
                                     status=new_task.status,
                                     time_estimation=new_task.time_estimation)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="created successfully",
                        status_code=status.HTTP_201_CREATED)


@router.patch('/update-task-title')
async def update_task_title(task: UpdateTaskNameSchema,
                            uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        await TaskService().update_task_title(uow=uow, old_name=task.old_title, new_name=task.new_title)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="updated successfully",
                        status_code=status.HTTP_200_OK)


@router.delete('/delete-task')
async def delete_task(task: DeleteTaskSchema,
                      uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        await TaskService().delete_task(uow=uow, title=task.title)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="deleted successfully",
                        status_code=status.HTTP_200_OK)
