import logging
from pathlib import Path
from typing import Literal

import pandas as pd
from sqlalchemy import select
from sqlalchemy.engine import Engine

from scripts.core.data_transformations import (
    create_additional_materials_df,
    create_course_series_df,
    create_courses_df,
    create_formats_df,
    create_handouts_df,
    create_languages_df,
    create_levels_df,
    create_prerequisites_df,
    create_series_df,
    preprocess_dataframe,
)
from techconnect_classes_api.core.config import get_setting
from techconnect_classes_api.database import (
    get_engine,
    get_managed_db,
    get_sqlalchemy_db_url,
)
from techconnect_classes_api.database.db import ModelType
from techconnect_classes_api.models import (
    AdditionalMaterial,
    Course,
    CourseSeries,
    Format,
    Handout,
    Language,
    Level,
    Prerequisite,
    Series,
)

log = logging.getLogger(__name__)


def validate_inserted_row_nums(table_model: ModelType, df: pd.DataFrame) -> bool:
    with get_managed_db() as session:
        db_table = session.scalars(select(table_model)).all()

    if len(db_table) != len(df):
        log.error(
            f"Incorrect rows in {table_model.__tablename__} table: {len(db_table)}; df: {len(df)}"
        )
        return False
    log.info(f"'{table_model.__tablename__}' validated")
    return True


def seed_table_one(
    df_to_seed: pd.DataFrame,
    table_name: str,
    connection: Engine,
    if_exists: Literal["fail", "replace", "append"] = "append",
    **kwargs,
) -> None:
    df_to_seed.to_sql(
        name=table_name, con=connection, index=False, if_exists=if_exists, **kwargs
    )
    log.info(f"'{table_name}' seeded")


def seed_database(env: str, resource_file_path: Path) -> None:
    settings = get_setting(env)
    db_url = get_sqlalchemy_db_url(settings)
    engine = get_engine(db_url)

    course_info = pd.read_csv(resource_file_path)
    course_info = preprocess_dataframe(course_info)

    # Seed data
    levels_df = create_levels_df(course_info)
    seed_table_one(levels_df, "levels", connection=engine, method="multi")

    formats_df = create_formats_df(course_info)
    seed_table_one(formats_df, "formats", connection=engine, method="multi")

    series_df = create_series_df(course_info)
    seed_table_one(series_df, "series", connection=engine, method="multi")

    languages_df = create_languages_df(course_info)
    seed_table_one(languages_df, "languages", connection=engine, method="multi")

    courses_df = create_courses_df(course_info)
    seed_table_one(courses_df, "courses", connection=engine, method="multi")

    prerequisites_df = create_prerequisites_df(course_info)
    seed_table_one(prerequisites_df, "prerequisites", connection=engine, method="multi")

    handouts_df = create_handouts_df(course_info)
    seed_table_one(handouts_df, "handouts", connection=engine, method="multi")

    additional_materials_df = create_additional_materials_df(course_info)
    seed_table_one(
        additional_materials_df,
        "additional_materials",
        connection=engine,
        method="multi",
    )

    course_series_df = create_course_series_df(course_info)
    seed_table_one(course_series_df, "course_series", connection=engine, method="multi")

    # Validate data
    validate_inserted_row_nums(Level, levels_df)
    validate_inserted_row_nums(Format, formats_df)
    validate_inserted_row_nums(Series, series_df)
    validate_inserted_row_nums(Language, languages_df)
    validate_inserted_row_nums(Course, courses_df)
    validate_inserted_row_nums(Prerequisite, prerequisites_df)
    validate_inserted_row_nums(Handout, handouts_df)
    validate_inserted_row_nums(AdditionalMaterial, additional_materials_df)
    validate_inserted_row_nums(CourseSeries, course_series_df)
