import os.path
import pytest

from src.ssg import app


class TestMain:
    def test_main_init(self):
        args = app.parse_args(["--create"])
        assert args.create is True

    def test_create_project_only_with_defaults(self, monkeypatch):

        def mockinput():
            return app.get_input()

        monkeypatch.setattr("app.get_input", lambda: "")

        assert app.create_project() == app.DEFAULT_SETTINGS
