import pathlib
import unittest

from .assets import results
from .utils_for_testing import asset

from ..src import structures


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = structures.Library(asset("basic_paths.toml"))

    def test_empty_library(self):
        """The library of posts."""
        library = structures.Library()
        self.assertEqual(library.size, 0)
        self.assertEqual(library.flat_tree, None)

    def test_empty_library_with_path(self):
        """The website map is defined in a toml file."""
        library = structures.Library(asset("TestLibrary/paths.toml"))
        self.assertEqual(library.flat_tree, results.test_flat_paths)

    def test_library_with_path_and_posts(self):
        """Posts added to the library will be tested against the paths when added."""
        library = structures.Library(asset("basic_paths.toml"))
        cases = {"simple_ok_post.toml": ('about:applications', 
                            '073032467b1bffb192b560d04f9b0192'),
                 "simple_ok_alternative_post.toml": ('about:getting_started', 
                             '87ce9d57e6f1a53a887e4834b9d620e0')}
        for case, attrs in cases.items():
            post = structures.Post(asset(case), website_path=library.flat_tree)
            library.add_post(post)
            self.assertEqual(library.flat_tree[attrs[0]], {attrs[1]: post})
        self.assertEqual(library.size, 2)

    def test_library_retrieve_post_content(self):
        """The library will manage the posts, so, retrieving a post's content is the library's function."""
        library = structures.Library(asset("basic_paths.toml"))
        post = structures.Post(asset("simple_ok_post.toml"), website_path=library.flat_tree)
        library.add_post(post)
        self.assertEqual(library.get_post(post.id), post)
