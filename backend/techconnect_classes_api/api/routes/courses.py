from typing import Annotated

from fastapi import APIRouter, Depends

from .limiter import limiter

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/all", response_model=...)
@limiter.limit("1/second")
def get_all_courses(db: Session = Depends(...)):
    raise


@router.get("/{course_id}", response_model=...)
@limiter.limit("1/second")
def get_course_info(course_id: int, db: Session = Depends(...)):
    raise


@router.get("/search", response_model=...)
@limiter.limit("1/second")
def search_courses(
    q: Annotated[str],
    topic: str,
    limit: int,
    offset: int,
    db: Session = Depends(...),
):
    raise
