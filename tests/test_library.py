import io

import pytest

from src.sagu import library, post

from .assets import results
from .utils_for_testing import asset


class TestLibrary:
    @pytest.fixture
    def mock_library(self):
        return library.Library(asset("basic_paths.toml"))

    def test_empty_library(self):
        """The library of posts."""
        _library = library.Library()
        assert _library.size == 0
        assert _library.flat_tree is None

    def test_passing_no_toml_file(self):
        """The website path must be defined in a toml file."""
        with pytest.raises(library.InvalidPathFileError):
            with io.StringIO(initial_value="Invalid") as invalid_file:
                library.Library(invalid_file)
        with pytest.raises(library.InvalidPathFileError):
            with io.BytesIO(b"Invalid") as invalid_file:
                library.Library(invalid_file)

    def test_empty_library_with_useless_entries(self):
        """The website map must generate a flat dict with empty dicts as values."""
        with pytest.raises(library.InvalidPathFileError):
            _library = library.Library(asset("TestLibrary/paths_with_useless.toml"))

    def test_empty_library_with_path(self):
        """The website map is defined in a toml file."""
        _library = library.Library(asset("TestLibrary/paths.toml"))
        assert _library.flat_tree == results.test_flat_paths

    @pytest.mark.skip("Not implemented yet.")
    def test_library_post_no_path(self, mock_library):
        assert False

    def test_library_with_path_and_posts(self, mock_library):
        """Posts added to the library will be tested against the paths when added."""
        cases = {
            "simple_ok_post.toml": (
                "about:applications",
                frozenset(("073032467b1bffb192b560d04f9b0192", "document-with-slug"))
                ),
            "simple_ok_alternative_post.toml": (
                "about:getting_started",
                frozenset(("87ce9d57e6f1a53a887e4834b9d620e0", "document-3"))
                ),
        }
        for case, attrs in cases.items():
            _post = post.Post(asset(case), website_path=mock_library.flat_tree)
            mock_library.add_post(_post)
            assert mock_library.flat_tree[attrs[0]] == {attrs[1]: _post}
        assert mock_library.size == 2

    def test_library_get_post_by_id(self, mock_library):
        _post = post.Post(asset("simple_ok_post.toml"), website_path=mock_library.flat_tree)
        mock_library.add_post(_post)
        assert mock_library.get_post_by_id("073032467b1bffb192b560d04f9b0192") == _post

    def test_get_post_by_slug(self, mock_library):
        _post = post.Post(asset("simple_ok_post.toml"), website_path=mock_library.flat_tree)
        mock_library.add_post(_post)
        assert mock_library.get_post_by_slug("document-with-slug") == _post

    def test_library_retrieve_post_content(self, mock_library):
        """The library will manage the posts, so, retrieving a post's content is the library's function."""
        _post = post.Post(asset("simple_ok_post.toml"), website_path=mock_library.flat_tree)
        mock_library.add_post(_post)
        assert mock_library.get_post_by_id(_post.id) == _post
        assert mock_library.get_post_by_slug(_post.slug) == _post

    def test_flatten(self):
        cases = [
                ({"A": {}}, {"A": {}}),
                ({"A": {"B": {}}}, {"A": {}, "A:B": {}}),
                ({"A": {"B": {"C": {}}}}, {"A": {}, "A:B": {}, "A:B:C": {}}),
        ]
        lib = library.Library()
        for case in cases:
            assert lib.flatten(case[0]) == case[1]
