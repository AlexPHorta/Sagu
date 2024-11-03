from ..src import app


class TestMain:
    def test_main_init(self):
        args = app.parse_args(["--create"])
        assert args.create is True
