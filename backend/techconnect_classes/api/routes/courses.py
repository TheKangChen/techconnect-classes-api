from typing import Annotated
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/all", response_model=...)
def get_all_courses(db: Session = Depends(...)):
    raise


@router.get("/{course_id}", response_model=...)
def get_course_info(course_id: int, db: Session = Depends(...)):
    raise


@router.get("/search", response_model=...)
def search_courses(
    q: Annotated[str],
    topic: str,
    limit: int,
    offset: int,
    db: Session = Depends(...),
):
    raise
