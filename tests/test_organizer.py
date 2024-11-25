import pytest

from src.ssg import structures

from .utils_for_testing import asset, equal_dirs, temporary_folder


class TestOrganizer:
    @pytest.fixture
    def post1(self):
        return structures.Post(asset("simple_ok_post.toml"))

    @pytest.fixture
    def post2(self):
        return structures.Post(asset("simple_ok_alternative_post.toml"))

    @pytest.fixture
    def library(self, post1, post2):
        library = structures.Library(asset("basic_paths.toml"))
        library.add_post(post1)
        library.add_post(post2)
        return library

    @pytest.fixture
    def builder(self):
        return structures.Builder(asset("TestBuilder/"))

    @pytest.fixture
    def template(self, builder):
        return builder.env.get_template("index.jinja")

    @pytest.fixture
    def organizer(self, library, builder):
        return structures.Organizer(library, builder)

    def test_organizer(self, builder, library, organizer):
        assert organizer.library == library
        assert organizer.builder == builder

    def test_organizer_gen_output(self, organizer):
        # Filenames follow the title when no slug specified.
        ignores = ["index.jinja", "index.toml"]
        with temporary_folder() as temp:
            organizer.gen_output(temp)
            assert equal_dirs(temp, asset("TestOrganizer"), ignore=ignores) is True
