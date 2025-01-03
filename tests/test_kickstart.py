import pathlib

import pytest
import tomllib

from src.sagu import kickstart

from .utils_for_testing import asset, equal_dirs, temporary_folder


@pytest.fixture(scope="module")
def mock_user_settings():
    return {
        "main_directory": "/home/documents/testproject",
        "SITENAME": "Test Project",
        "SITEAUTHOR": "Test Author",
        "SITELANGUAGE": "pt",
        "SITEURL": "www.example.com",
        "SITETIMEZONE": "America/Sao_Paulo",
    }


class TestGetInput:
    def test_get_input_prompt(self, monkeypatch):
        expected_prompt = "Enter something: "

        def mock_input(prompt):
            assert prompt == expected_prompt
            return "mocked input"

        monkeypatch.setattr("builtins.input", mock_input)

        result = kickstart.get_input(prompt=expected_prompt)

        assert result == "mocked input"

    def test_user_input(self):
        assert kickstart.get_input(user_input="Test input") == "Test input"
        assert kickstart.get_input(user_input=123456) == "123456"
        assert kickstart.get_input(user_input=[123456]) == "[123456]"

    def test_user_input_and_prompt(self):
        assert kickstart.get_input(user_input="Test input", prompt="No need for that") == "Test input"


class TestGetUserSettings:
    def test_get_user_settings_only_with_defaults(self, monkeypatch):
        def mock_input(prompt):  # noqa: ARG001
            return ""

        monkeypatch.setattr("builtins.input", mock_input)

        result = kickstart.get_user_settings()

        assert result == dict([kv[0] for kv in kickstart.DEFAULT_SETTINGS])

    def test_get_user_settings_with_user_info(self, mock_user_settings, monkeypatch):
        inputs = iter(mock_user_settings.values())

        def mock_input(prompt):  # noqa: ARG001
            return next(inputs)

        monkeypatch.setattr("builtins.input", mock_input)

        result = kickstart.get_user_settings()

        assert result == mock_user_settings


class TestGenerateProject:
    def test_generate_project_with_non_existent_folder(self, mock_user_settings, monkeypatch):
        new_settings = mock_user_settings
        new_directory = "test/within/testproject"
        new_settings["main_directory"] = new_directory

        with temporary_folder() as temp:
            monkeypatch.chdir(temp)

            kickstart.generate_project(new_settings)
            project = pathlib.PurePath(new_directory)
            assert pathlib.Path(project).resolve().exists() is True

    def test_generate_project_with_defaults(self, mock_user_settings, monkeypatch):
        new_settings = mock_user_settings
        new_directory = "."
        new_settings["main_directory"] = new_directory

        with temporary_folder() as temp:
            monkeypatch.chdir(temp)

            kickstart.generate_project(new_settings)
            project = pathlib.PurePath("testproject")
            assert pathlib.Path(project).resolve().exists() is True

    # @pytest.mark.skip("Skip until I have a final solution for the base theme.")
    def test_generate_project_full(self, mock_user_settings, monkeypatch):
        new_settings = mock_user_settings
        new_directory = "."
        new_settings["main_directory"] = new_directory
        new_settings["SITENAME"] = "Título com Acento"
        new_settings["SITEAUTHOR"] = "Cebolinha"
        new_settings["SITELANGUAGE"] = "fr"
        new_settings["SITEURL"] = "www.cebolinhateste.com"
        new_settings["SITETIMEZONE"] = "America/Sao_Paulo"

        with temporary_folder() as temp:
            monkeypatch.chdir(temp)

            kickstart.generate_project(new_settings)
            assert equal_dirs(temp, asset("TestGenerateProject"), ignore=["settings.toml"]) is True
            with open(pathlib.Path(temp, asset("TestGenerateProject"), "titulocomacento/settings.toml"), "rb") as t:
                assert tomllib.load(t) == new_settings


class TestNormalizeName:
    def test_normalize(self):
        assert kickstart.normalize_name("") == ""
        assert kickstart.normalize_name("á") == "a"
        assert kickstart.normalize_name("Título") == "titulo"
        assert kickstart.normalize_name("Straße") == "strasse"
