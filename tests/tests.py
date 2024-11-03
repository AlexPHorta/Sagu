import filecmp

import pytest

from ..src import structures
from .utils_for_testing import asset, equal_dirs, temporary_folder


class TestBuilder:

    def test_builder(self):
        """The builder will manage the mixing of posts and templates."""
        builder = structures.Builder(asset("TestBuilder/"))
        template = builder.env.get_template("basic.jinja")
        assert template.render(name="Test") == "Hello, Test!\n"

    def test_builder_autoescape_off(self):
        """The builder will have autoescape turned off by default."""
        builder = structures.Builder(asset("TestBuilder/"))
        assert builder.env.autoescape is False

    def test_builder_build_post(self):
        library = structures.Library(asset("basic_paths.toml"))
        post = structures.Post(asset("TestBuilder/index.toml"),
                        website_path=library.flat_tree)
        library.add_post(post)
        builder = structures.Builder(asset("TestBuilder/"))
        template = builder.env.get_template("index.jinja")
        with open(asset("TestBuilder/index.html")) as f:
            test_builder_post = library.get_post(post.id)
            assert template.render(test_builder_post.get_contents()) == f.read()

class TestOrganizer:

    pytest.fixture()
    def post1(self):
        return structures.Post(asset("simple_ok_post.toml"))

    pytest.fixture()
    def post2(self):
        return structures.Post(asset("simple_ok_alternative_post.toml"))

    pytest.fixture()
    def library(self, post1, post2):
        library = structures.Library(asset("basic_paths.toml"))
        library.add_post(post1)
        library.add_post(post2)
        return library

    pytest.fixture()
    def builder(self):
        return structures.Builder(asset("TestBuilder/"))

    pytest.fixture()
    def template(self, builder):
        return builder.env.get_template("index.jinja")

    pytest.fixture()
    def organizer(self):
        return structures.Organizer(self.library, self.builder)

    def test_organizer(self, builder, library, organizer):
        assert organizer.library == library
        assert organizer.builder == builder

    def test_organizer_gen_output(self, organizer):
        # Filenames follow the title when no slug specified.
        ignores = ['index.jinja', 'index.toml']
        with temporary_folder() as temp:
            organizer.gen_output(temp)
            compare = filecmp.dircmp(temp, asset("TestOrganizer"), ignore=ignores)
            assert equal_dirs(compare) is True
