from src.ssg import builder, library, post

from .utils_for_testing import asset


class TestBuilder:
    def test_builder(self, capsys):
        """The builder will manage the mixing of posts and templates."""
        _builder = builder.Builder(asset("TestBuilder/"))
        template = _builder.env.get_template("basic.jinja")
        assert template.render(name="Test") == "Hello, Test!\n"

    def test_builder_autoescape_on(self):
        """The builder will have autoescape turned on by default."""
        _builder = builder.Builder(asset("TestBuilder/"))
        assert _builder.env.autoescape is True

    def test_builder_build_post(self):
        _library = library.Library(asset("basic_paths.toml"))
        _post = post.Post(asset("TestBuilder/index.toml"), website_path=_library.flat_tree)
        _library.add_post(_post)
        _builder = builder.Builder(asset("TestBuilder/"))
        template = _builder.env.get_template("index.jinja")
        with open(asset("TestBuilder/index.html")) as f:
            test_builder_post = _library.get_post(_post.id)
            assert template.render(test_builder_post.get_contents()) == f.read()
