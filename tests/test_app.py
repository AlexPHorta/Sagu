import pytest

from .context import src


class TestMain:
    def test_main_init(self):
        args = src.app.parse_args(["--create"])
        assert args.create is True

    def test_create_project_only_with_defaults(self, monkeypatch):

        def mockinput():
            return src.app.get_input()

        monkeypatch.setattr("src.app.get_input", lambda: "")

        assert src.app.create_project() == src.app.DEFAULT_SETTINGS
