from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from src.services.department_service import DepartmentService
from src.schemas.department import DepartmentSchema, UpdateDepartmentSchema
from src.auth.utils.auth_utils import get_current_auth_user
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/v1", tags=["Department"],
                   dependencies=[Depends(get_current_auth_user)]
                   )


@router.post('/add-department')
async def add_department(new_department: DepartmentSchema) -> JSONResponse:
    try:
        await DepartmentService().add_department(department_name=new_department.name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="created successfully",
                        status_code=status.HTTP_201_CREATED)


@router.put('/update-department')
async def update_department(department: UpdateDepartmentSchema, uow: UnitOfWork = Depends(UnitOfWork)) -> JSONResponse:
    try:
        await DepartmentService().update_department(uow=uow, _id=department.id, name=department.name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="updated successfully",
                        status_code=status.HTTP_201_CREATED)


@router.delete('/delete-department')
async def delete_department(_id: int, uow: UnitOfWork = Depends(UnitOfWork)) -> JSONResponse:
    try:
        await DepartmentService().delete_department(uow=uow, _id=_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="deleted successfully",
                        status_code=status.HTTP_200_OK)


@router.put('/change-struct')
async def change_struct(_id: int):
    await DepartmentService().change_struct(_id=_id)
