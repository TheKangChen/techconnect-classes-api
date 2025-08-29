from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from techconnect_classes_api.api.limiter import limiter
from techconnect_classes_api.crud.course import course_crud
from techconnect_classes_api.database import get_db
from techconnect_classes_api.schemas.course import (
    CourseAdditionalMaterialsResponse,
    CourseDetailResponse,
    CourseFormatsResponse,
    CourseHandoutsResponse,
    CourseLanguagesResponse,
    CourseLevelsResponse,
    CourseNodeQuery,
    CourseNodeResponse,
    CourseSeriesResponse,
)

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get(
    "/all", response_model=list[CourseNodeResponse], status_code=status.HTTP_200_OK
)
@limiter.limit("1/second")
def fetch_all_courses(
    query_params: Annotated[CourseNodeQuery, Query()],
    db: Annotated[Session, Depends(get_db)],
):
    """Fetch all courses.

    Parameters:
        db (Session): The database session.
        query_params (CourseNodeQuery):
            level: Course level.
            format: Course format.
            series: Course series/topic.
            search: Keyword for searching course name in databse.
    Returns:
        List of courses with their id.
    """
    return course_crud.get_multiple_filtered(db, query_params=query_params)


@router.get(
    "/{course_id}/handouts",
    response_model=CourseHandoutsResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("1/second")
def fetch_handouts_by_id(
    course_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
):
    """Fetch handouts by course id.

    Parameters:
        course_id (Path): Course id.
        db (Session): The database session.
    Returns:
        list of handouts.
    """
    return course_crud.get_handouts(db, course_id=course_id)


@router.get(
    "/{course_id}/additional-materials",
    response_model=CourseAdditionalMaterialsResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("1/second")
def fetch_additional_materials_by_id(
    course_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
):
    return course_crud.get_additional_materials(db, course_id=course_id)


@router.get("/{course_id}/upcoming", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
@limiter.limit("1/second")
def redirect_to_upcoming_session_link_by_id(
    course_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
):
    url = course_crud.get_upcoming(db, course_id=course_id)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upcoming session link not found for this course.",
        )
    return RedirectResponse(url=str(url))


@router.get(
    "/{course_id}", response_model=CourseDetailResponse, status_code=status.HTTP_200_OK
)
@limiter.limit("1/second")
def fetch_course_detail(
    course_id: Annotated[int, Path()], db: Annotated[Session, Depends(get_db)]
):
    return course_crud.get_detail(db, course_id)


@router.get(
    "/formats", response_model=CourseFormatsResponse, status_code=status.HTTP_200_OK
)
@limiter.limit("1/second")
def fetch_all_course_formats(db: Annotated[Session, Depends(get_db)]):
    return course_crud.get_all_formats(db)


@router.get(
    "/formats", response_model=CourseLanguagesResponse, status_code=status.HTTP_200_OK
)
@limiter.limit("1/second")
def fetch_all_course_languages(db: Annotated[Session, Depends(get_db)]):
    return course_crud.get_all_languages(db)


@router.get(
    "/formats", response_model=CourseLevelsResponse, status_code=status.HTTP_200_OK
)
@limiter.limit("1/second")
def fetch_all_course_levels(db: Annotated[Session, Depends(get_db)]):
    return course_crud.get_all_levels(db)


@router.get(
    "/formats", response_model=CourseSeriesResponse, status_code=status.HTTP_200_OK
)
@limiter.limit("1/second")
def fetch_all_course_series(db: Annotated[Session, Depends(get_db)]):
    return course_crud.get_all_series(db)
