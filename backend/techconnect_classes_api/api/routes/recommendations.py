from fastapi import APIRouter, Depends

from .limiter import limiter

router = APIRouter(prefix="/me", tags=["recommendation"])


@router.get("/recommendation", response_model=...)
@limiter.limit("1/second")
def get_user_recommendation():
    raise
