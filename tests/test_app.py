import argparse

import pytest

from src.ssg import app
from .utils_for_testing import asset, equal_dirs, temporary_folder


class TestMain:
    def test_main_kickstart(self):
        args = app.parse_args(["--create"])
        assert args.create is True

    def test_main_generate(self):
        args = app.parse_args(["--generate"])
        assert args.generate is True

    def test_main_kickstart_or_generate(self):
        """Create and generate form a mutually exclusive group."""
        with pytest.raises(SystemExit) as exc:
            app.parse_args(["--create", "--generate"])

    def test_main_generate_website(self):
        with temporary_folder() as temp:
            assert False
            # assert equal_dirs(temp, asset("TestOrganizer"), ignore=ignores) is True
