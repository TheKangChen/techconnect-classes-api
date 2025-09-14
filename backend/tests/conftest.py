import pytest
import pandas as pd

from techconnect_classes_api.core.config import get_settings
from techconnect_classes_api.core.log import setup_logger


@pytest.fixture(scope="session", autouse=True)
def test_logger():
    setup_logger()


@pytest.fixture(scope="session")
def test_settings():
    yield get_settings("test")


@pytest.fixture(scope="session")
def raw_dataframe_fixture():
    data = {
        'class_title': [
            "Excel for Beginners",
            "Intermediate python functions",
            "Getting started with Canva",
            "Photoshop basics",
            "Open Lab",
            "Procreate Workshop: Create a brush",
        ],
        'description': [
            "Introductory course on excel meant for people with no experience with Microsoft Excel.",
            "Learn more about functions in Python, including variable length arguments, default parameters, and argument passing.",
            "Are you interested in making your own flyer or social media posts? Take this course to find out how to do it all with Canva!",
            "In this class, you will learn abou the fundamentals of using Photoshop as well as the core user interface.",
            "Come and get your computer related issues fixed.",
            "Create your very own painting brush inside procreate!",
        ],
        'handout': [
            "https://example.com/excel-1",
            None,
            None,
            "https://example.com/photoshop-basics",
            None,
            None,
        ],
        'handout_chinese': [
            "https://example.com/excel-1_zh",
            None,
            None,
            None,
            None,
            None,
        ],
        'handout_spanish': [
            "https://example.com/excel-1_es",
            None,
            None,
            None,
            None,
            None,
        ],
        'handout_bengali': [
            "https://example.com/excel-1_bn",
            None,
            None,
            None,
            None,
            None,
        ],
        'handout_french': [
            None,
            None,
            None,
            "https://example.com/photoshop-basics_fr",
            None,
            None,
        ],
        'handout_russian': [
            None,
            None,
            None,
            "https://example.com/photoshop-basics_ru",
            None,
            None,
        ],
        'additional_materials': [
            None,
            "https://codesandbox.io/example",
            None,
            None,
            None,
            None,
        ],
        'prerequisite': [
            None,
            "Excel for Beginners",
            "Photoshop basics",
            None,
            None,
            "Getting started with Canva",
        ],
        'level': [
            "Beginner",
            "Advanced",
            "Beginner",
            "Intermediate",
            "None",
            "Intermediate",
        ],
        'series': [
            "microsoft office, office software, microsoft excel",
            "python, programming",
            "graphic design, canva, media production",
            "photo editing, adobe photoshop, media production",
            "support",
            "ipad, digital art, media production, procreate",
        ],
        'format': [
            "class",
            "class",
            "class",
            "class",
            "lab",
            "workshop",
        ],
    }
    return pd.DataFrame(data)

@pytest.fixture(scope="function")
def preprocessed_dataframe_fixture():
    data = {
        'course_name': [
            "Excel For Beginners",
            "Intermediate Python Functions",
            "Getting Started With Canva",
            "Photoshop Basics",
            "Open Lab",
            "Procreate Workshop: Create A Brush",
        ],
        'description': [
            "Introductory course on excel meant for people with no experience with Microsoft Excel.",
            "Learn more about functions in Python, including variable length arguments, default parameters, and argument passing.",
            "Are you interested in making your own flyer or social media posts? Take this course to find out how to do it all with Canva!",
            "In this class, you will learn abou the fundamentals of using Photoshop as well as the core user interface.",
            "Come and get your computer related issues fixed.",
            "Create your very own painting brush inside procreate!",
        ],
        'handout': [
            "https://example.com/excel-1",
            None,
            None,
            "https://example.com/photoshop-basics",
            None,
            None,
        ],
        'handout_chinese': [
            "https://example.com/excel-1_zh",
            None,
            None,
            None,
            None,
            None,
        ],
        'handout_spanish': [
            "https://example.com/excel-1_es",
            None,
            None,
            None,
            None,
            None,
        ],
        'handout_bengali': [
            "https://example.com/excel-1_bn",
            None,
            None,
            None,
            None,
            None,
        ],
        'handout_french': [
            None,
            None,
            None,
            "https://example.com/photoshop-basics_fr",
            None,
            None,
        ],
        'handout_russian': [
            None,
            None,
            None,
            "https://example.com/photoshop-basics_ru",
            None,
            None,
        ],
        'additional_materials': [
            None,
            "https://codesandbox.io/example",
            None,
            None,
            None,
            None,
        ],
        'prerequisite': [
            None,
            "Excel For Beginners",
            "Photoshop Basics",
            None,
            None,
            "Getting Started With Canva",
        ],
        'level': [
            "Beginner",
            "Advanced",
            "Beginner",
            "Intermediate",
            "None",
            "Intermediate",
        ],
        'series': [
            "microsoft office, office software, microsoft excel",
            "python, programming",
            "graphic design, canva, media production",
            "photo editing, adobe photoshop, media production",
            "support",
            "ipad, digital art, media production, procreate",
        ],
        'format': [
            "class",
            "class",
            "class",
            "class",
            "lab",
            "workshop",
        ],
    }
    return pd.DataFrame(data)


class MockLevel:
    def __init__(self, id: int, level_name: str):
        self.id = id
        self.level_name = level_name


class MockFormat:
    def __init__(self, id: int, format_name: str):
        self.id = id
        self.format_name = format_name


class MockSeries:
    def __init__(self, id: int, series_name: str):
        self.id = id
        self.series_name = series_name


class MockLanguage:
    def __init__(self, language_code: str, language_name: str):
        self.language_code = language_code
        self.language_name = language_name


class MockCourse:
    def __init__(self, id: int, course_name: str, description: str, level_id: int, format_id: int):
        self.id = id
        self.course_name = course_name
        self.description = description
        self.level_id = level_id
        self.format_id = format_id


@pytest.fixture
def mock_levels_table_data():
    return [
        MockLevel(id=1, level_name="advanced"),
        MockLevel(id=2, level_name="beginner"),
        MockLevel(id=3, level_name="intermediate"),
        MockLevel(id=4, level_name="none"),
    ]


@pytest.fixture
def mock_formats_table_data():
    return [
        MockFormat(id=1, format_name="class"),
        MockFormat(id=2, format_name="lab"),
        MockFormat(id=3, format_name="workshop"),
    ]


@pytest.fixture
def mock_series_table_data():
    return [
        MockSeries(id=1, series_name='adobe photoshop'),
        MockSeries(id=2, series_name='canva'),
        MockSeries(id=3, series_name='digital art'),
        MockSeries(id=4, series_name='graphic design'),
        MockSeries(id=5, series_name='ipad'),
        MockSeries(id=6, series_name='media production'),
        MockSeries(id=7, series_name='microsoft excel'),
        MockSeries(id=8, series_name='microsoft office'),
        MockSeries(id=9, series_name='office software'),
        MockSeries(id=10, series_name='photo editing'),
        MockSeries(id=11, series_name='procreate'),
        MockSeries(id=12, series_name='programming'),
        MockSeries(id=13, series_name='python'),
        MockSeries(id=14, series_name='support'),
    ]


@pytest.fixture
def mock_languages_table_data():
    return [
        MockLanguage(language_code="en", language_name="english"),
        MockLanguage(language_code="zh", language_name="chinese"),
        MockLanguage(language_code="es", language_name="spanish"),
        MockLanguage(language_code="bn", language_name="bengali"),
        MockLanguage(language_code="fr", language_name="french"),
        MockLanguage(language_code="ru", language_name="russian"),
    ]


@pytest.fixture
def mock_courses_table_data():
    return [
        MockCourse(
            id=1,
            course_name="Excel For Beginners",
            description="Introductory course on excel meant for people with no experience with Microsoft Excel.",
            level_id=2,
            format_id=1
        ),
        MockCourse(
            id=2,
            course_name="Intermediate Python Functions",
            description="Learn more about functions in Python, including variable length arguments, default parameters, and argument passing.",
            level_id=1,
            format_id=1
        ),
        MockCourse(
            id=3,
            course_name="Getting Started With Canva",
            description="Are you interested in making your own flyer or social media posts? Take this course to find out how to do it all with Canva!",
            level_id=2,
            format_id=1
        ),
        MockCourse(
            id=4,
            course_name="Photoshop Basics",
            description="In this class, you will learn abou the fundamentals of using Photoshop as well as the core user interface.",
            level_id=3,
            format_id=1
        ),
        MockCourse(
            id=5,
            course_name="Open Lab",
            description="Come and get your computer related issues fixed.",
            level_id=4,
            format_id=2
        ),
        MockCourse(
            id=6,
            course_name="Procreate Workshop: Create A Brush",
            description="Create your very own painting brush inside procreate!",
            level_id=3,
            format_id=3
        ),
    ]
