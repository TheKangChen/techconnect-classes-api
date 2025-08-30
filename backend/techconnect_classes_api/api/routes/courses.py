from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
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


@router.get("/all", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
def fetch_all_courses(
    request: Request,
    query_params: Annotated[CourseNodeQuery, Query()],
    db: Annotated[Session, Depends(get_db)],
) -> list[CourseNodeResponse]:
    """Fetch all courses.

    Parameters:
        db (Session): The database session.
        query_params (CourseNodeQuery):
            level: Course level.
            format: Course format.
            series: Course series/topic.
            search: Keyword for searching course name in databse.
    Returns:
        list[CourseNodeResponse]: List of courses with their id.
    """
    return course_crud.get_multiple_filtered(db, query_params=query_params)


@router.get("/formats", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
def fetch_all_course_formats(
    request: Request, db: Annotated[Session, Depends(get_db)]
) -> CourseFormatsResponse:
    """Fetch all course formats.

    Parameters:
        db (Session): The database session.
    Returns:
        CourseFormatsResponse: All course formats.
    """
    return course_crud.get_all_formats(db)


@router.get("/languages", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
def fetch_all_course_languages(
    request: Request, db: Annotated[Session, Depends(get_db)]
) -> CourseLanguagesResponse:
    """Fetch all course languages.

    Parameters:
        db (Session): The database session.
    Returns:
        CourseLanguagesResponse: All course languages.
    """
    return course_crud.get_all_languages(db)


@router.get("/levels", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
def fetch_all_course_levels(
    request: Request, db: Annotated[Session, Depends(get_db)]
) -> CourseLevelsResponse:
    """Fetch all course levels.

    Parameters:
        db (Session): The database session.
    Returns:
        CourseLevelsResponse: All course levels.
    """
    return course_crud.get_all_levels(db)


@router.get("/series", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
def fetch_all_course_series(
    request: Request, db: Annotated[Session, Depends(get_db)]
) -> CourseSeriesResponse:
    """Fetch all course series/topics.

    Parameters:
        db (Session): The database session.
    Returns:
        CourseSeriesResponse: All course series/topics.
    """
    return course_crud.get_all_series(db)


@router.get(
    "/{course_id}/handouts",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("1/second")
def fetch_handouts_by_id(
    request: Request,
    course_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
) -> CourseHandoutsResponse | None:
    """Fetch handouts by course id.

    Parameters:
        course_id (Path): Course id.
        db (Session): The database session.
    Returns:
        CourseHandoutsResponse: Object containing a list of handout objects with language code and handout url.
    """
    return course_crud.get_handouts(db, course_id=course_id)


@router.get(
    "/{course_id}/additional-materials",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("1/second")
def fetch_additional_materials_by_id(
    request: Request,
    course_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
) -> CourseAdditionalMaterialsResponse | None:
    """Fetch additional materials by course id.

    Parameters:
        course_id (Path): Course id.
        db (Session): The database session.
    Returns:
        CourseAdditionalMaterialsResponse: Object containing a list of additional material urls.
    """
    return course_crud.get_additional_materials(db, course_id=course_id)


@router.get(
    "/{course_id}/upcoming",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
@limiter.limit("1/second")
def redirect_to_upcoming_session_link_by_id(
    request: Request,
    course_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
) -> RedirectResponse:
    """Fetch additional materials by course id.

    Parameters:
        course_id (Path): Course id.
        db (Session): The database session.
    Returns:
        RedirectResponse: To NYPL TechConnect page of upcoming classes.
    """
    url = course_crud.get_upcoming(db, course_id=course_id)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upcoming session link not found for this course.",
        )
    return RedirectResponse(url=str(url))


@router.get("/{course_id}", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
def fetch_course_detail(
    request: Request,
    course_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
) -> CourseDetailResponse | None:
    """Fetch course detailed information by course id.

    Parameters:
        course_id (Path): Course id.
        db (Session): The database session.
    Returns:
        CourseDetailResponse: Object containing all course detail.
    """
    return course_crud.get_detail(db, course_id)
