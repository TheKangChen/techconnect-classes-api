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
            "Python Container Datatypes",
            None,
            "studio40 Orientation 101 & 201",
            None,
            "Learn to Draw with Procreate Part 2",
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
            "Python Container Datatypes",
            None,
            "Studio40 Orientation 101 & 201",
            None,
            "Learn To Draw With Procreate Part 2",
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
