import filecmp
import pathlib

import pytest

from src.ssg import app

from .utils_for_testing import asset, equal_dirs, temporary_folder


@pytest.fixture(scope="module")
def mock_user_settings():
    return {
        "main_directory": "/home/documents/testproject",
        "website_title": "Test Project",
        "website_author": "Test Author",
        "website_language": "pt",
        "website_url": "www.example.com",
        "website_timezone": "America/Sao_Paulo",
    }


class TestGetInput:
    def test_get_input_prompt(self, monkeypatch):
        expected_prompt = "Enter something: "

        def mock_input(prompt):
            assert prompt == expected_prompt
            return "mocked input"

        monkeypatch.setattr("builtins.input", mock_input)

        result = app.get_input(prompt=expected_prompt)

        assert result == "mocked input"

    def test_user_input(self):
        assert app.get_input(user_input="Test input") == "Test input"
        assert app.get_input(user_input=123456) == "123456"
        assert app.get_input(user_input=[123456]) == "[123456]"

    def test_user_input_and_prompt(self):
        assert app.get_input(user_input="Test input", prompt="No need for that") == "Test input"


class TestMain:
    def test_main_init(self):
        args = app.parse_args(["--create"])
        assert args.create is True


class TestGetUserSettings:
    def test_get_user_settings_only_with_defaults(self, monkeypatch):
        def mock_input(prompt):  # noqa: ARG001
            return ""

        monkeypatch.setattr("builtins.input", mock_input)

        result = app.get_user_settings()

        assert result == dict([kv[0] for kv in app.DEFAULT_SETTINGS])

    def test_get_user_settings_with_user_info(self, mock_user_settings, monkeypatch):
        inputs = iter(mock_user_settings.values())

        def mock_input(prompt):  # noqa: ARG001
            return next(inputs)

        monkeypatch.setattr("builtins.input", mock_input)

        result = app.get_user_settings()

        assert result == mock_user_settings


class TestGenerateProject:
    def test_generate_project_with_non_existent_folder(self, mock_user_settings, monkeypatch):
        new_settings = mock_user_settings
        new_directory = "test/within/testproject"
        new_settings["main_directory"] = new_directory

        with temporary_folder() as temp:
            monkeypatch.chdir(temp)

            app.generate_project(new_settings)
            project = pathlib.PurePath(new_directory)
            assert pathlib.Path(project).resolve().exists() is True

    def test_generate_project_with_defaults(self, mock_user_settings, monkeypatch):
        new_settings = mock_user_settings
        new_directory = "."
        new_settings["main_directory"] = new_directory

        with temporary_folder() as temp:
            monkeypatch.chdir(temp)

            app.generate_project(new_settings)
            project = pathlib.PurePath("testproject")
            assert pathlib.Path(project).resolve().exists() is True

    def test_generate_project_full(self, mock_user_settings, monkeypatch):
        new_settings = mock_user_settings
        new_directory = "."
        new_settings["main_directory"] = new_directory

        with temporary_folder() as temp:
            monkeypatch.chdir(temp)

            app.generate_project(new_settings)
            compare = filecmp.dircmp(temp, asset("TestGenerateProject"))
            assert equal_dirs(compare) is True
