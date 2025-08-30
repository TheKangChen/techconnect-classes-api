from fastapi import APIRouter, Depends

from techconnect_classes_api.api.limiter import limiter

# router = APIRouter(prefix="/users", tags=["users"])
#
#
# @router.get("/me", response_model=...)
# @limiter.limit("1/second")
# def get_user_info():
#     raise
#
#
# @router.post("/me", response_model=...)
# @limiter.limit("1/second")
# def create_user_info():
#     raise
#
#
# @router.patch("/me", response_model=...)
# @limiter.limit("1/second")
# def update_user_info():
#     raise
#
#
# @router.delete("/me", response_model=...)
# @limiter.limit("1/second")
# def delete_user_info():
#     raise
