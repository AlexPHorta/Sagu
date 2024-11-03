import datetime

import pytest

from .assets import results
from .context import src
from .utils_for_testing import asset


class TestPost:
    @pytest.fixture
    def post(self):
        return src.structures.Post(asset("basic.toml"))

    def test_reader(self, post):
        """Read the post's toml file and generate the post object."""
        assert post.reader(post.post_path) == results.basic

    def test_basic_post(self, post):
        """A basic post has the title, the creation date, and the content."""
        attributes = {
            "id": "161b7313299edeaa9a130fea6021382f",
            "title": "Document title",
            "creation_date": datetime.datetime(2024, 9, 22, 10, 27),  # noqa: DTZ001
            "last_update": datetime.datetime(2024, 9, 22, 10, 27),  # noqa: DTZ001
            "raw_content": results.basic["content"],
            "author": None,
            "authors": None,
            "category": None,
            "tags": None,
            "keywords": None,
            "slug": None,
            "summary": None,
            "status": None,
            "path": None,
            "filename": "document-title",
        }
        for attr in attributes:
            assert getattr(post, attr) == attributes[attr]

    def test_wrong_post_format(self):
        """Check if there's meta and content tables."""
        cases = ("wrong_meta.toml", "no_meta.toml", "wrong_content.toml", "no_content.toml")
        for case in cases:
            with pytest.raises(src.structures.InvalidMapSectionsError):
                src.structures.Post(asset("TestReader/" + case))

    def test_post_with_path(self):
        """A post with a path defined will be tested against the website's paths."""
        library = src.structures.Library(asset("basic_paths.toml"))
        post = src.structures.Post(asset("simple_ok_post.toml"))
        assert post.path in library.flat_tree

    def test_post_with_wrong_parent_path(self):
        """A post with a wrong path will trigger an exception."""
        library = src.structures.Library(asset("basic_paths.toml"))
        with pytest.raises(KeyError):
            src.structures.Post(asset("wrong_parent_path.toml"), website_path=library.flat_tree)

    def test_post_content_markdown(self):
        """Retrieve a post with markdown content."""
        library = src.structures.Library(asset("basic_paths.toml"))
        post = src.structures.Post(asset("simple_ok_post_with_markdown_content.toml"), website_path=library.flat_tree)
        assert post.content == results.content_markdown

    def test_post_with_slug(self):
        """The slug, if present, defines the post's filename."""
        post = src.structures.Post(asset("simple_ok_post.toml"))
        assert post.filename == "document-with-slug"

    def test_post_slug_with_one_unsafe_character(self):
        """An invalid slug makes the filename fallback to the title."""
        post = src.structures.Post(asset("simple_post_unsafe_slug.toml"))
        assert post.filename == "document-1"


class TestSanitize:
    def test_sanitize(self):
        assert src.structures.sanitize(None) is None
        assert src.structures.sanitize("") is None
        assert src.structures.sanitize("$") is None
        assert src.structures.sanitize(" ") is None
        assert src.structures.sanitize("-") is None
        assert src.structures.sanitize(src.structures.RESERVED_AND_UNSAFE) is None
        assert src.structures.sanitize(0) == "0"
        assert src.structures.sanitize("a") == "a"
        assert src.structures.sanitize("A") == "a"
        assert src.structures.sanitize("A a") == "a-a"
        assert src.structures.sanitize("A A") == "a-a"
        assert src.structures.sanitize("Te$t") == "tet"
        assert src.structures.sanitize("Te$t 2") == "tet-2"
        assert src.structures.sanitize("2 Te$t") == "2-tet"
        assert src.structures.sanitize("Last Test Indeed") == "last-test-indeed"
