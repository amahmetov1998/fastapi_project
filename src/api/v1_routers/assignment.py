from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from src.services.assign_service import AssignService
from src.schemas.assignment import AssignLeaderSchema, AssignUserSchema, ReassignSchema
from src.auth.utils.auth_utils import get_current_auth_user
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/v1", tags=["Assignment"], dependencies=[Depends(get_current_auth_user)])


@router.post('/assign-leader')
async def assign_leader(data: AssignLeaderSchema, uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        await AssignService().assign_leader(uow=uow,
                                            position_name=data.position_name,
                                            department_name=data.department_name,
                                            first_name=data.first_name,
                                            last_name=data.last_name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="assigned successfully",
                        status_code=status.HTTP_201_CREATED)


@router.patch('/assign-worker')
async def assign_worker(data: AssignUserSchema, uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        await AssignService().assign_user(uow=uow,
                                          position_name=data.position_name,
                                          leader_position=data.leader_position,
                                          first_name=data.first_name,
                                          last_name=data.last_name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="assigned successfully",
                        status_code=status.HTTP_201_CREATED)


@router.patch('/reassign-user')
async def reassign_user(data: ReassignSchema, uow: UnitOfWork = Depends(UnitOfWork)):
    try:
        await AssignService().reassign_user(uow=uow,
                                            position_name=data.position_name,
                                            first_name=data.first_name,
                                            last_name=data.last_name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="reassigned successfully",
                        status_code=status.HTTP_200_OK)
