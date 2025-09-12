import pandas as pd

from scripts.core.data_transformations import (
    create_formats_df,
    create_languages_df,
    create_levels_df,
    create_series_df,
    preprocess_dataframe,
)


def test_preprocess_dataframe(raw_dataframe_fixture, preprocessed_dataframe_fixture):
    """Sanity check we're not getting weird issues from data transformations."""
    res_df = preprocess_dataframe(raw_dataframe_fixture)

    assert not res_df.empty
    assert "course_name" in res_df.columns
    assert res_df["course_name"].isna().sum() == 0
    assert res_df["description"].isna().sum() == 0
    assert res_df["level"].isna().sum() == 0
    assert res_df["series"].isna().sum() == 0
    assert res_df["format"].isna().sum() == 0

    pd.testing.assert_frame_equal(res_df, preprocessed_dataframe_fixture)


def test_create_levels_df(preprocessed_dataframe_fixture):
    res_df = create_levels_df(preprocessed_dataframe_fixture)

    assert isinstance(res_df, pd.Series)
    assert not res_df.empty
    assert res_df.name == "level_name"
    assert res_df.to_list() == ['advanced', 'beginner', 'intermediate', 'none']


def test_create_formats_df(preprocessed_dataframe_fixture):
    res_df = create_formats_df(preprocessed_dataframe_fixture)

    assert isinstance(res_df, pd.Series)
    assert not res_df.empty
    assert res_df.name == "format_name"
    assert res_df.to_list() == ['class', 'lab', 'workshop']


def test_create_series_df(preprocessed_dataframe_fixture):
    res_df = create_series_df(preprocessed_dataframe_fixture)

    assert isinstance(res_df, pd.Series)
    assert not res_df.empty
    assert res_df.name == "series_name"
    assert not res_df.duplicated().any()


def test_create_languages_df(preprocessed_dataframe_fixture):
    res_df = create_languages_df(preprocessed_dataframe_fixture)

    assert isinstance(res_df, pd.DataFrame)
    assert not res_df.empty
    assert list(res_df.columns) == ["language_code", "language_name"]
    assert res_df.language_code.to_list() == ['en', 'zh', 'es', 'bn', 'fr', 'ru']
    assert res_df.language_name.to_list() == ['english', 'chinese', 'spanish', 'bengali', 'french', 'russian']


# NOTE: Probably need mocking/patching for db_session
# def test_create_courses_df(): raise
# def test_create_prerequisites_df(): raise
# def test_create_handouts_df(): raise
# def test_create_lang_handout_df(): raise
# def test_create_additional_materials_df(): raise
# def test_create_course_series_df(): raise
