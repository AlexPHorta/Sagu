import pytest

from src.ssg import app


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

    # def test_create_project_only_with_defaults(self, monkeypatch):
    #     def mockinput():
    #         return app.get_input()

    #     monkeypatch.setattr("app.get_input", lambda: "")

    #     assert app.create_project() == app.DEFAULT_SETTINGS
