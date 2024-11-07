import pytest

from src.ssg import app
from .utils_for_testing import asset, equal_dirs, temporary_folder


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
        def mock_input(prompt):
            return ""

        monkeypatch.setattr("builtins.input", mock_input)

        result = app.get_user_settings()

        assert result == app.DEFAULT_SETTINGS

    def test_get_user_settings_with_user_info(self, monkeypatch):
        inputs = iter(['/home/documents/testproject', 'Test Project', 'Test Author', 'pt', 'www.example.com', 'America/Sao_Paulo'])

        def mock_input(prompt):
            return next(inputs)

        monkeypatch.setattr("builtins.input", mock_input)

        result = app.get_user_settings()

        assert result == {
                        "main_directory": "/home/documents/testproject",
                        "website_title": "Test Project",
                        "website_author": "Test Author",
                        "website_language": "pt",
                        "website_url": "www.example.com",
                        "website_timezone": "America/Sao_Paulo",
                        }


class TestGenerateProject:
    def test_generate_project_with_defaults(self, monkeypatch):
        def mock_input(prompt):
            return ""
        monkeypatch.setattr("builtins.input", mock_input)
        user_settings = app.get_user_settings()

        with temporary_folder() as temp:
            app.generate_project(temp, user_settings["website_title"])
            compare = filecmp.dircmp(temp, asset("TestGenerateProject"), ignore=ignores)
            assert equal_dirs(compare) is True

