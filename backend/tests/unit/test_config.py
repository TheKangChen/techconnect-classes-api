import os
from dotenv import load_dotenv

load_dotenv(".env.test")


def test_config(test_settings):
    for key, value in test_settings.model_dump().items():
        assert str(value) == os.environ[key]
