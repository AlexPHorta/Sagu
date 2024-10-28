import datetime
import pathlib
import unittest

from .assets import results
from .utils_for_testing import asset, equal_dirs, temporary_folder

from src import ssg


class TestPost(unittest.TestCase):

    def setUp(self):
        self.post = ssg.Post(asset("basic.toml"))

    def test_reader(self):
        """Read the post's toml file and generate the post object."""
        self.assertEqual(self.post.reader(self.post.post_path), 
            results.basic)

    def test_basic_post(self):
        """A basic post has the title, the creation date, and the content."""
        attributes = {"id": '161b7313299edeaa9a130fea6021382f', 
            "title": "Document title", 
            "creation_date": datetime.datetime(2024, 9, 22, 10, 27), 
            "last_update": datetime.datetime(2024, 9, 22, 10, 27),
            "raw_content": results.basic["content"], "author": None, 
            "authors": None, "category": None, "tags": None, "keywords": None, 
            "slug": None, "summary": None, "status": None, "path": None, 
            "filename": "document-title"}
        for attr in attributes:
            self.assertEqual(getattr(self.post, attr), attributes[attr])

    def test_wrong_post_format(self):
        """Check if there's meta and content tables."""
        with self.assertRaises(KeyError):
            cases = ('wrong_meta.toml', 'no_meta.toml', 'wrong_content.toml', 
                     'no_content.toml')
            for case in cases:
                ssg.Post(asset("TestReader/" + case))

    def test_post_with_path(self):
        """A post with a path defined will be tested against the website's paths."""
        library = ssg.Library(asset("basic_paths.toml"))
        post = ssg.Post(asset("simple_ok_post.toml"))
        self.assertTrue(post.path in library.flat_tree)

    def test_post_with_wrong_parent_path(self):
        """A post with a wrong path will trigger an exception."""
        library = ssg.Library(asset("basic_paths.toml"))
        with self.assertRaises(KeyError):
            ssg.Post(asset("wrong_parent_path.toml"), website_path=library.flat_tree)

    def test_post_content_markdown(self):
        """Retrieve a post with markdown content."""
        library = ssg.Library(asset("basic_paths.toml"))
        post = ssg.Post(asset("simple_ok_post_with_markdown_content.toml"), 
                              website_path=library.flat_tree)
        self.assertEqual(post.content, results.content_markdown)

    def test_post_with_slug(self):
        """The slug, if present, defines the post's filename."""
        post = ssg.Post(asset("simple_ok_post.toml"))
        self.assertEqual(post.filename, "document-with-slug")

    def test_post_slug_with_one_unsafe_character(self):
        """An invalid slug makes the filename fallback to the title."""
        post = ssg.Post(asset("simple_post_unsafe_slug.toml"))
        self.assertEqual(post.filename, "document-1")


class TestSanitize(unittest.TestCase):

    def test_sanitize(self):
        self.assertEqual(ssg.sanitize(None), None)
        self.assertEqual(ssg.sanitize(""), None)
        self.assertEqual(ssg.sanitize("$"), None)
        self.assertEqual(ssg.sanitize(" "), None)
        self.assertEqual(ssg.sanitize("-"), None)
        self.assertEqual(ssg.sanitize(ssg.RESERVED_AND_UNSAFE), None)
        self.assertEqual(ssg.sanitize(0), "0")
        self.assertEqual(ssg.sanitize("a"), "a")
        self.assertEqual(ssg.sanitize("A"), "a")
        self.assertEqual(ssg.sanitize("A a"), "a-a")
        self.assertEqual(ssg.sanitize("A A"), "a-a")
        self.assertEqual(ssg.sanitize("Te$t"), "tet")
        self.assertEqual(ssg.sanitize("Te$t 2"), "tet-2")
        self.assertEqual(ssg.sanitize("2 Te$t"), "2-tet")
        self.assertEqual(ssg.sanitize("Last Test Indeed"), "last-test-indeed")
