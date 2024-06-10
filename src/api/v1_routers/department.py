from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from src.services.department_service import DepartmentService
from src.schemas.department import DepartmentSchema
from src.auth.utils.auth_utils import get_current_auth_user
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/v1", tags=["Department"], dependencies=[Depends(get_current_auth_user)])


@router.post('/add-department')
async def add_department(new_department: DepartmentSchema):
    try:
        await DepartmentService().add_department(department_name=new_department.name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="department already exists")

    return JSONResponse(content="created successfully",
                        status_code=status.HTTP_201_CREATED)


@router.delete('/delete-department')
async def delete_department(department: DepartmentSchema, uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        await DepartmentService().delete_department(uow=uow, department_name=department.name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="")

    return JSONResponse(content="deleted successfully",
                        status_code=status.HTTP_201_CREATED)
