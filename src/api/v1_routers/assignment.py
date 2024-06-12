from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from src.services.assign_service import AssignService
from src.schemas.assignment import AssignLeaderSchema, AssignUserSchema, ReassignUserSchema
from src.auth.utils.auth_utils import get_current_auth_user
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/v1", tags=["Assignment"], dependencies=[Depends(get_current_auth_user)])


@router.post('/assign-leader')
async def assign_leader(data: AssignLeaderSchema, uow: UnitOfWork = Depends(UnitOfWork)) -> JSONResponse:
    try:
        await AssignService().assign_leader(uow=uow,
                                            position_id=data.position_id,
                                            department_id=data.department_id,
                                            user_id=data.user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="assigned successfully",
                        status_code=status.HTTP_201_CREATED)


@router.post('/assign-worker')
async def assign_worker(data: AssignUserSchema, uow: UnitOfWork = Depends(UnitOfWork)) -> JSONResponse:
    try:
        await AssignService().assign_user(uow=uow,
                                          position_id=data.position_id,
                                          leader_position_id=data.leader_position_id,
                                          user_id=data.user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="assigned successfully",
                        status_code=status.HTTP_201_CREATED)


@router.put('/reassign-user')
async def reassign_user(data: ReassignUserSchema, uow: UnitOfWork = Depends(UnitOfWork)) -> JSONResponse:
    try:
        await AssignService().reassign_user(uow=uow,
                                            position_id=data.position_id,
                                            user_id=data.user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="invalid data")

    return JSONResponse(content="reassigned successfully",
                        status_code=status.HTTP_200_OK)
