import unittest

from ..src import app


class TestMain(unittest.TestCase):

    def test_main_init(self):
        args = app.parse_args(['--create'])
        self.assertTrue(args.create)
