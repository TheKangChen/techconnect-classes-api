import logging
from typing import Annotated

import langcodes
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from techconnect_classes_api.database import get_managed_db
from techconnect_classes_api.models import Course, Format, Language, Level, Series

log = logging.getLogger(__name__)


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    processed_df = df.rename(columns={"class_title": "course_name"})

    # Handle course name casing
    processed_df["course_name"] = processed_df["course_name"].str.title()
    processed_df["prerequisite"] = processed_df["prerequisite"].str.title()

    # Handle null values
    processed_df["level"] = processed_df["level"].fillna("None")

    # Check null values
    if processed_df["course_name"].isna().sum() != 0:
        raise AssertionError(
            f"Column course_name includes null values: {processed_df.course_name.isna().sum()}"
        )

    if processed_df["description"].isna().sum() != 0:
        raise AssertionError(
            f"Column description includes null values: {processed_df.description.isna().sum()}"
        )

    if processed_df["level"].isna().sum() != 0:
        raise AssertionError(
            f"Column level includes null values: {processed_df.level.isna().sum()}"
        )

    if processed_df["series"].isna().sum() != 0:
        raise AssertionError(
            f"Column series includes null values: {processed_df.series.isna().sum()}"
        )

    if processed_df["format"].isna().sum() != 0:
        raise AssertionError(
            f"Column format includes null values: {processed_df.format.isna().sum()}"
        )

    return processed_df


def create_levels_df(df: pd.DataFrame) -> pd.DataFrame:
    levels = (
        df["level"]
        .copy()
        .str.lower()
        .str.strip()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )
    levels.name = "level_name"
    return levels


def create_formats_df(df: pd.DataFrame) -> pd.DataFrame:
    formats = (
        df["format"]
        .copy()
        .str.strip()
        .str.lower()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )
    formats.name = "format_name"
    return formats


def create_series_df(df: pd.DataFrame) -> pd.DataFrame:
    series = (
        df["series"]
        .copy()
        .str.split(", ")
        .explode()
        .str.lower()
        .str.strip()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )
    series.name = "series_name"
    return series


def create_languages_df(df: pd.DataFrame) -> pd.DataFrame:
    handout_langs = [
        col.replace("handout_", "").replace("handout", "english")
        for col in df.columns
        if "handout" in col
    ]
    try:
        handout_langs = [
            (langcodes.find(lang).language, lang) for lang in handout_langs
        ]
    except LookupError as e:
        log.info(f"Error mapping language to language code: {e}")
        raise
    return pd.DataFrame(data=handout_langs, columns=["language_code", "language_name"])


def create_courses_df(df: pd.DataFrame) -> pd.DataFrame:
    courses = df[["course_name", "description", "level", "format"]].copy()

    # Get level id & format id from database
    with get_managed_db() as session:
        db_levels = session.scalars(select(Level)).all()
        level_id_mapping = {lvl.level_name: lvl.id for lvl in db_levels}
        db_formats = session.scalars(select(Format)).all()
        format_id_mapping = {fmt.format_name: fmt.id for fmt in db_formats}

    log.debug(level_id_mapping)
    log.debug(format_id_mapping)

    # Create level_id & format_id column with id mappings
    courses["level_id"] = (
        courses["level"].str.strip().str.lower().map(level_id_mapping).astype("Int64")
    )
    courses["format_id"] = (
        courses["format"].str.strip().str.lower().map(format_id_mapping).astype("Int64")
    )

    # Check for null values
    if courses["level_id"].isna().sum() != 0:
        raise AssertionError(
            f"Column level_id includes null values: {courses.level_id.isna().sum()}"
        )
    if courses["format_id"].isna().sum() != 0:
        raise AssertionError(
            f"Column format_id includes null values: {courses.format_id.isna().sum()}"
        )

    # Check if foreign key value counts match original value counts
    level_counts = courses["level"].str.strip().str.lower().value_counts()
    level_id_counts = courses["level_id"].value_counts()

    if sorted(level_counts.tolist()) == sorted(level_id_counts.tolist()):
        courses = courses.drop(columns=["level"])
    else:
        raise AssertionError(f"""WARNING: Mismatch detected between Level and Level_ID counts.
          Counts for original level names: {level_counts.sort_values().tolist()}
          Counts for new level IDs: {level_id_counts.sort_values().tolist()}""")

    format_counts = courses["format"].str.strip().str.lower().value_counts()
    format_id_counts = courses["format_id"].value_counts()

    if sorted(format_counts.tolist()) == sorted(format_id_counts.tolist()):
        courses.drop(columns=["format"], inplace=True)
    else:
        raise AssertionError(f"""WARNING: Mismatch detected between format and format_id counts.
          Counts for original format names: {format_counts.sort_values().tolist()}
          Counts for new format IDs: {format_id_counts.sort_values().tolist()}""")
    return courses


def create_prerequisites_df(df: pd.DataFrame) -> pd.DataFrame:
    prerequisites = df[["course_name", "prerequisite"]].dropna().copy()

    # Get course id from database
    with get_managed_db() as session:
        db_courses = session.scalars(select(Course)).all()
        course_id_mapping = {c.course_name: c.id for c in db_courses}

    prerequisites["course_id"] = (
        prerequisites["course_name"].map(course_id_mapping).astype("Int64")
    )
    prerequisites["prereq_id"] = (
        prerequisites["prerequisite"].map(course_id_mapping).astype("Int64")
    )

    # Check id count equals name count
    course_counts = prerequisites["course_name"].str.strip().str.lower().value_counts()
    course_id_counts = prerequisites["course_id"].value_counts()

    if sorted(course_counts.tolist()) == sorted(course_id_counts.tolist()):
        prerequisites = prerequisites.drop(columns=["course_name"])
    else:
        raise AssertionError(f"""WARNING: Mismatch detected between course_name and course_id counts.
          Counts for original course names: {course_counts.sort_values().tolist()}
          Counts for new course IDs: {course_id_counts.sort_values().tolist()}""")

    prereq_counts = prerequisites["prerequisite"].str.strip().str.lower().value_counts()
    prereq_id_counts = prerequisites["prereq_id"].value_counts()

    if sorted(prereq_counts.tolist()) == sorted(prereq_id_counts.tolist()):
        prerequisites = prerequisites.drop(columns=["prerequisite"])
    else:
        raise AssertionError(f"""WARNING: Mismatch detected between prerequisite and prereq_id counts.
          Counts for original prerequisite names: {prereq_counts.sort_values().tolist()}
          Counts for new prereq IDs: {prereq_id_counts.sort_values().tolist()}""")

    prerequisites.reset_index(drop=True)
    return prerequisites


def create_handouts_df(df: pd.DataFrame) -> pd.DataFrame:
    def create_lang_handout_df(
        handouts_df: Annotated[pd.DataFrame, "Processed handouts dataframe"],
        handout_language: str,
        db_session: Session,
    ) -> pd.DataFrame:
        """Return dataframe of handouts in specified language with course_name, url, language_code as columns."""

        lang_ho_df = handouts_df[["course_name", handout_language]].copy().dropna()
        lang_obj = db_session.execute(
            select(Language.language_name, Language.language_code).where(
                Language.language_name == handout_language
            )
        ).one()
        lang_ho_df["language_code"] = lang_obj.language_code
        lang_ho_df = lang_ho_df.rename(columns={ho_lang: "url"})
        log.debug(
            f"{handout_language} handout dataframe created: {lang_obj.language_code}"
        )
        return lang_ho_df

    # Get all handout columns in dataframe with mask
    handout_columns = [col for col in df.columns if "handout" in col]
    ho_col_name_map = {
        col: col.replace("handout_", "").replace("handout", "english")
        for col in handout_columns
    }
    mask = ["course_name"] + handout_columns

    handouts = df[mask].copy().dropna(subset=handout_columns, how="all")
    handouts = handouts.rename(columns=ho_col_name_map)

    with get_managed_db() as session:
        # English df
        ho_lang = "english"
        en_handouts = create_lang_handout_df(handouts, ho_lang, session)

        # Chinese df
        ho_lang = "chinese"
        zh_handouts = create_lang_handout_df(handouts, ho_lang, session)

        # Spanish df
        ho_lang = "spanish"
        es_handouts = create_lang_handout_df(handouts, ho_lang, session)

        # Bengali df
        ho_lang = "bengali"
        bn_handouts = create_lang_handout_df(handouts, ho_lang, session)

        # French df
        ho_lang = "french"
        fr_handouts = create_lang_handout_df(handouts, ho_lang, session)

        # Russian df
        ho_lang = "russian"
        ru_handouts = create_lang_handout_df(handouts, ho_lang, session)

    # Merge all language dataframes into one
    combined_handouts = pd.concat(
        [en_handouts, zh_handouts, es_handouts, bn_handouts, fr_handouts, ru_handouts],
        ignore_index=True,
    )

    with get_managed_db() as session:
        db_courses = session.scalars(select(Course)).all()
        course_id_mapping = {c.course_name: c.id for c in db_courses}

    # Add course_id column
    combined_handouts["course_id"] = (
        combined_handouts["course_name"].map(course_id_mapping).astype("Int64")
    )

    # Check
    course_counts = (
        combined_handouts["course_name"].str.strip().str.lower().value_counts()
    )
    course_id_counts = combined_handouts["course_id"].value_counts()

    if sorted(course_counts.tolist()) == sorted(course_id_counts.tolist()):
        combined_handouts = combined_handouts.drop(columns=["course_name"])
    else:
        raise AssertionError(f"""WARNING: Mismatch detected between course_name and course_id counts.
          Counts for original course_name names: {course_counts.sort_values().tolist()}
          Counts for new course IDs: {course_id_counts.sort_values().tolist()}""")

    return combined_handouts


def create_additional_materials_df(df: pd.DataFrame) -> pd.DataFrame:
    additional_materials = df[["course_name", "additional_materials"]].copy().dropna()
    additional_materials = additional_materials.rename(
        columns={"additional_materials": "url"}
    )

    # Add course_id column
    with get_managed_db() as session:
        db_courses = session.scalars(select(Course)).all()
        course_id_mapping = {c.course_name: c.id for c in db_courses}

    additional_materials["course_id"] = (
        additional_materials["course_name"].map(course_id_mapping).astype("Int64")
    )

    # Check if number of course name match course id
    course_counts = (
        additional_materials["course_name"].str.strip().str.lower().value_counts()
    )
    course_id_counts = additional_materials["course_id"].value_counts()

    if sorted(course_counts.tolist()) == sorted(course_id_counts.tolist()):
        additional_materials = additional_materials.drop(columns=["course_name"])
    else:
        raise AssertionError(f"""WARNING: Mismatch detected between course_name and course_id counts.
          Counts for original course_name names: {course_counts.sort_values().tolist()}
          Counts for new course IDs: {course_id_counts.sort_values().tolist()}""")

    return additional_materials


def create_course_series_df(df: pd.DataFrame) -> pd.DataFrame:
    course_series = df[["course_name", "series"]].copy()

    course_series["series"] = course_series["series"].str.split(", ")
    exploded_course_series = course_series.explode("series")
    exploded_course_series["series"] = (
        exploded_course_series["series"].str.strip().str.lower()
    )
    exploded_course_series = exploded_course_series.drop_duplicates()

    with get_managed_db() as session:
        db_courses = session.scalars(select(Course)).all()
        course_id_mapping = {c.course_name: c.id for c in db_courses}

        db_series = session.scalars(select(Series)).all()
        series_id_mapping = {s.series_name: s.id for s in db_series}

    # Add course_id
    exploded_course_series["course_id"] = (
        exploded_course_series["course_name"].map(course_id_mapping).astype("Int64")
    )

    # series_id column
    exploded_course_series["series_id"] = (
        exploded_course_series["series"].map(series_id_mapping).astype("Int64")
    )

    # Check
    course_counts = (
        exploded_course_series["course_name"].str.strip().str.lower().value_counts()
    )
    course_id_counts = exploded_course_series["course_id"].value_counts()

    if sorted(course_counts.tolist()) == sorted(course_id_counts.tolist()):
        exploded_course_series = exploded_course_series.drop(columns=["course_name"])
    else:
        raise AssertionError(f"""WARNING: Mismatch detected between course_name and course_id counts.
          Counts for original course_name names: {course_counts.sort_values().tolist()}
          Counts for new course IDs: {course_id_counts.sort_values().tolist()}""")

    series_counts = (
        exploded_course_series["series"].str.strip().str.lower().value_counts()
    )
    series_id_counts = exploded_course_series["series_id"].value_counts()

    if sorted(series_counts.tolist()) == sorted(series_id_counts.tolist()):
        exploded_course_series = exploded_course_series.drop(columns=["series"])
    else:
        raise AssertionError(f"""WARNING: Mismatch detected between series and series_id counts.
          Counts for original series names: {series_counts.sort_values().tolist()}
          Counts for new series IDs: {series_id_counts.sort_values().tolist()}""")

    return exploded_course_series
