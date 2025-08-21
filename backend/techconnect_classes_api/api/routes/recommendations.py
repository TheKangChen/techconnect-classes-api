from fastapi import APIRouter, Depends

router = APIRouter(prefix="/me", tags=["recommendation"])


@router.get("/recommendation", response_model=...)
def get_user_recommendation():
    raise
