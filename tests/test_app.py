import os.path
import pytest

from .context import ssg

print(dir(ssg))


class TestMain:
    def test_main_init(self):
        args = ssg.app.parse_args(["--create"])
        assert args.create is True

    def test_create_project_only_with_defaults(self, monkeypatch):

        def mockinput():
            return ssg.app.get_input()

        monkeypatch.setattr("ssg.app.get_input", lambda: "")

        assert ssg.app.create_project() == ssg.app.DEFAULT_SETTINGS
