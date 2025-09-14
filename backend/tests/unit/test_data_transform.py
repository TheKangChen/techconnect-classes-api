import pandas as pd

from unittest.mock import patch, MagicMock

from scripts.core.data_transformations import (
    create_formats_df,
    create_languages_df,
    create_levels_df,
    create_series_df,
    preprocess_dataframe,
    create_courses_df,
    create_prerequisites_df,
    create_handouts_df,
    create_additional_materials_df,
    create_course_series_df,
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


@patch("scripts.core.data_transformations.get_managed_db")
def test_create_courses_df(mock_get_db, mock_levels_table_data, mock_formats_table_data, preprocessed_dataframe_fixture):
    # Mock database session and calls to return a fixture
    mock_session = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.side_effect = [mock_levels_table_data, mock_formats_table_data]
    mock_session.scalars.return_value = mock_scalars
    mock_get_db.return_value.__enter__.return_value = mock_session

    res_df = create_courses_df(preprocessed_dataframe_fixture)

    expected_df = pd.DataFrame({
        "course_name": [
            "Excel For Beginners",
            "Intermediate Python Functions",
            "Getting Started With Canva",
            "Photoshop Basics",
            "Open Lab",
            "Procreate Workshop: Create A Brush",
        ],
        "description": [
            "Introductory course on excel meant for people with no experience with Microsoft Excel.",
            "Learn more about functions in Python, including variable length arguments, default parameters, and argument passing.",
            "Are you interested in making your own flyer or social media posts? Take this course to find out how to do it all with Canva!",
            "In this class, you will learn abou the fundamentals of using Photoshop as well as the core user interface.",
            "Come and get your computer related issues fixed.",
            "Create your very own painting brush inside procreate!",
        ],
        "level_id": pd.Series([
            2,
            1,
            2,
            3,
            4,
            3,
        ], dtype="Int64"),
        "format_id": pd.Series([
            1,
            1,
            1,
            1,
            2,
            3,
        ], dtype="Int64"),
    })

    pd.testing.assert_frame_equal(res_df, expected_df, check_like=True)
    

@patch("scripts.core.data_transformations.get_managed_db")
def test_create_prerequisites_df(mock_get_db, mock_courses_table_data, preprocessed_dataframe_fixture):
    mock_session = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.side_effect = [mock_courses_table_data]
    mock_session.scalars.return_value = mock_scalars
    mock_get_db.return_value.__enter__.return_value = mock_session

    # Reset index cause index is ignored when writing to db in seed_table function
    res_df = create_prerequisites_df(preprocessed_dataframe_fixture).reset_index(drop=True)

    expected_df = pd.DataFrame({
        "course_id": pd.Series([2, 3, 6], dtype="Int64"),
        "prereq_id": pd.Series([1, 4, 3], dtype="Int64"),
    })
    print(res_df)
    print(expected_df)

    pd.testing.assert_frame_equal(res_df, expected_df, check_index_type=False, check_like=True)


@patch("scripts.core.data_transformations.get_managed_db")
def test_create_handouts_df(mock_get_db, mock_languages_table_data, mock_courses_table_data, preprocessed_dataframe_fixture):
    mock_session = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = mock_courses_table_data
    mock_session.scalars.return_value = mock_scalars
    mock_get_db.return_value.__enter__.return_value = mock_session

    def mock_execute_side_effect(statement, *args, **kwargs):
        # Check query to see which language is being requested
        lang_name = statement.whereclause.right.value
        
        mock_result = MagicMock()
        mock_result.one.return_value = mock_languages_table_data[lang_name]
        return mock_result

    mock_session.execute.side_effect = mock_execute_side_effect

    res_df = create_handouts_df(preprocessed_dataframe_fixture).reset_index(drop=True)

    expected_df = pd.DataFrame({
        "url": [
            "https://example.com/excel-1",
            "https://example.com/excel-1_zh",
            "https://example.com/excel-1_es",
            "https://example.com/excel-1_bn",
            "https://example.com/photoshop-basics",
            "https://example.com/photoshop-basics_fr",
            "https://example.com/photoshop-basics_ru",
        ],
        "language_code": ["en", "zh", "es", "bn", "en", "fr", "ru"],
        "course_id": pd.Series([1, 1, 1, 1, 4, 4, 4], dtype="Int64"),
    })

    # Sort cause the order doesn't matter
    res_df_sorted = res_df.sort_values(
        by=["course_id", "language_code"], ignore_index=True
    )
    expected_df_sorted = expected_df.sort_values(
        by=["course_id", "language_code"], ignore_index=True
    )

    pd.testing.assert_frame_equal(res_df_sorted, expected_df_sorted, check_like=True)


@patch("scripts.core.data_transformations.get_managed_db")
def test_create_additional_materials_df(mock_get_db, mock_courses_table_data, preprocessed_dataframe_fixture):
    mock_session = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.side_effect = [mock_courses_table_data]
    mock_session.scalars.return_value = mock_scalars
    mock_get_db.return_value.__enter__.return_value = mock_session

    res_df = create_additional_materials_df(preprocessed_dataframe_fixture).reset_index(drop=True)

    expected_df = pd.DataFrame({
        "url": ["https://codesandbox.io/example"],
        "course_id": pd.Series([2], dtype="Int64"),
    })

    pd.testing.assert_frame_equal(res_df, expected_df)


@patch("scripts.core.data_transformations.get_managed_db")
def test_create_course_series_df(mock_get_db, mock_courses_table_data, mock_series_table_data, preprocessed_dataframe_fixture):
    mock_session = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.side_effect = [mock_courses_table_data, mock_series_table_data]
    mock_session.scalars.return_value = mock_scalars
    mock_get_db.return_value.__enter__.return_value = mock_session

    res_df = create_course_series_df(preprocessed_dataframe_fixture).reset_index(drop=True)

    expected_df = pd.DataFrame({
        "course_id": pd.Series([1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 6, 6, 6, 6], dtype="Int64"),
        "series_id": pd.Series([8, 9, 7, 13, 12, 4, 2, 6, 10, 1, 6, 14, 5, 3, 6, 11], dtype="Int64"),
    })

    pd.testing.assert_frame_equal(res_df, expected_df, check_like=True)
