from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=...)
def get_user_info():
    raise


@router.post("/me", response_model=...)
def create_user_info():
    raise


@router.patch("/me", response_model=...)
def update_user_info():
    raise


@router.delete("/me", response_model=...)
def delete_user_info():
    raise
