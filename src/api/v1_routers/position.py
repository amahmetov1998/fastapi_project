from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from src.services.position_service import PositionService
from src.schemas.position import AddPositionSchema, UpdatePositionSchema
from src.auth.utils.auth_utils import get_current_auth_user
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/v1", tags=["Create position"], dependencies=[Depends(get_current_auth_user)])


@router.post('/add-position')
async def add_position(new_position: AddPositionSchema,
                       uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        await PositionService().add_position(uow=uow,
                                             department_name=new_position.department_name,
                                             position_name=new_position.position_name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="position already exists")

    return JSONResponse(content="created successfully",
                        status_code=status.HTTP_201_CREATED)


@router.post('/update-position')
async def update_position(position: UpdatePositionSchema,
                          uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        await PositionService().update_position(uow=uow,
                                                old_position_name=position.old_position_name,
                                                new_position_name=position.new_position_name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="")

    return JSONResponse(content="updated successfully",
                        status_code=status.HTTP_201_CREATED)
