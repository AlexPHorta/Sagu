import pytest

from src.ssg import builder, library, organizer, post

from .utils_for_testing import asset, equal_dirs, temporary_folder


class TestOrganizer:
    @pytest.fixture
    def post1(self):
        return post.Post(asset("simple_ok_post.toml"))

    @pytest.fixture
    def post2(self):
        return post.Post(asset("simple_ok_alternative_post.toml"))

    @pytest.fixture
    def mock_library(self, post1, post2):
        _library = library.Library(asset("basic_paths.toml"))
        _library.add_post(post1)
        _library.add_post(post2)
        return _library

    @pytest.fixture
    def mock_builder(self):
        return builder.Builder(asset("TestBuilder/"))

    @pytest.fixture
    def template(self, mock_builder):
        return mock_builder.env.get_template("index.jinja")

    @pytest.fixture
    def mock_organizer(self, mock_library, mock_builder):
        return organizer.Organizer(mock_library, mock_builder)

    def test_organizer(self, mock_builder, mock_library, mock_organizer):
        assert mock_organizer.library == mock_library
        assert mock_organizer.builder == mock_builder

    def test_organizer_gen_output(self, mock_organizer):
        # Filenames follow the title when no slug specified.
        ignores = ["index.jinja", "index.toml"]
        with temporary_folder() as temp:
            mock_organizer.gen_output(temp)
            assert equal_dirs(temp, asset("TestOrganizer"), ignore=ignores) is True
