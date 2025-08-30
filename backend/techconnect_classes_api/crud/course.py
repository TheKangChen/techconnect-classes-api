from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.orm import Session

from techconnect_classes_api.models import Course, Format, Language, Level, Series
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
    HandoutResponse,
)

from .base import CRUDBase


class CourseCRUD(CRUDBase[Course, None, None]):
    def get_multiple_filtered(
        self, db: Session, query_params: CourseNodeQuery
    ) -> list[CourseNodeResponse]:
        db_query = db.query(self.model)

        if query_params.level:
            db_query = db_query.join(Level).filter(
                self.model.level == query_params.level
            )

        if query_params.format:
            db_query = db_query.join(Format).filter(
                Format.format_name == query_params.format
            )

        if query_params.series:
            db_query = (
                db_query.join(self.model.courses_in_series)
                .join(Series)
                .filter(Series.series_name == query_params.series)
                .distinct()
            )

        if query_params.search:
            search_term = f"%{query_params.series.lower()}%"
            db_query = db_query.filter(self.model.course_name.ilike(search_term))

        db_courses = db_query.all()

        return [CourseNodeResponse.model_validate(course) for course in db_courses]

    def get_detail(self, db: Session, course_id: int) -> CourseDetailResponse | None:
        db_course = (
            db.query(self.model)
            .join(self.model.courses_in_series)
            .join(Series)
            .filter(self.model.id == course_id)
            .one_or_none()
        )

        if not db_course:
            return None

        series_names = [s.series.series_name for s in db_course.courses_in_series]

        prereq_names = [p.prereq_course.course_name for p in db_course.prereqs]

        upcoming_sessions_link = f"https://www.nypl.org/techconnect?keyword={db_course.course_name.replace(' ', '+')}"

        return CourseDetailResponse(
            course_name=db_course.course_name,
            description=db_course.description,
            series=series_names,
            level=db_course.level,
            format=db_course.format,
            prereqs=prereq_names,
            available_handouts=db_course.handouts,
            additional_materials=db_course.additional_materials,
            link_to_upcoming_sessions=HttpUrl(upcoming_sessions_link),
        )

    def get_upcoming(self, db: Session, course_id: int) -> HttpUrl | None:
        db_course = (
            db.query(self.model).filter(self.model.id == course_id).one_or_none()
        )

        if not db_course:
            return None

        return HttpUrl(
            f"https://www.nypl.org/techconnect?keyword={db_course.course_name.replace(' ', '+')}"
        )

    def get_handouts(
        self, db: Session, course_id: int
    ) -> CourseHandoutsResponse | None:
        db_course = (
            db.query(self.model).filter(self.model.id == course_id).one_or_none()
        )

        if not db_course:
            return None

        handout_schemas = [
            HandoutResponse(language_code=h.language_code, url=h.url)
            for h in db_course.handouts
        ]

        return CourseHandoutsResponse(handouts=handout_schemas)

    def get_additional_materials(
        self, db: Session, course_id: int
    ) -> CourseAdditionalMaterialsResponse | None:
        db_course = (
            db.query(self.model).filter(self.model.id == course_id).one_or_none()
        )

        if not db_course:
            return None

        return CourseAdditionalMaterialsResponse(
            additional_materials=db_course.additional_materials
        )

    def get_all_formats(self, db: Session) -> CourseFormatsResponse:
        db_formats = db.scalars(select(Format)).all()
        return CourseFormatsResponse(formats=[str(f.format_name) for f in db_formats])

    def get_all_levels(self, db: Session) -> CourseLevelsResponse:
        db_levels = db.scalars(select(Level)).all()
        return CourseLevelsResponse(
            levels=[str(level.level_name) for level in db_levels]
        )

    def get_all_series(self, db: Session) -> CourseSeriesResponse:
        db_series = db.scalars(select(Series)).all()
        return CourseSeriesResponse(series=[str(s.series_name) for s in db_series])

    def get_all_languages(self, db: Session) -> CourseLanguagesResponse:
        db_langs = db.scalars(select(Language)).all()
        return CourseLanguagesResponse(
            languages={
                str(lang.language_name): str(lang.language_code) for lang in db_langs
            }
        )


course_crud = CourseCRUD(model=Course)
