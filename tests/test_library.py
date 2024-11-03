import pytest

from .assets import results
from .context import src
from .utils_for_testing import asset


class TestLibrary:
    @pytest.fixture
    def library(self):
        return src.structures.Library(asset("basic_paths.toml"))

    def test_empty_library(self):
        """The library of posts."""
        library = src.structures.Library()
        assert library.size == 0
        assert library.flat_tree is None

    def test_empty_library_with_path(self):
        """The website map is defined in a toml file."""
        library = src.structures.Library(asset("TestLibrary/paths.toml"))
        assert library.flat_tree == results.test_flat_paths

    def test_library_with_path_and_posts(self, library):
        """Posts added to the library will be tested against the paths when added."""
        cases = {
            "simple_ok_post.toml": ("about:applications", "073032467b1bffb192b560d04f9b0192"),
            "simple_ok_alternative_post.toml": ("about:getting_started", "87ce9d57e6f1a53a887e4834b9d620e0"),
        }
        for case, attrs in cases.items():
            post = src.structures.Post(asset(case), website_path=library.flat_tree)
            library.add_post(post)
            assert library.flat_tree[attrs[0]] == {attrs[1]: post}
        assert library.size == 2

    def test_library_retrieve_post_content(self, library):
        """The library will manage the posts, so, retrieving a post's content is the library's function."""
        post = src.structures.Post(asset("simple_ok_post.toml"), website_path=library.flat_tree)
        library.add_post(post)
        assert library.get_post(post.id) == post
