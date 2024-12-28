import datetime

import pytest

from src.ssg import library, post

from .assets import results
from .utils_for_testing import asset


class TestPost:
    @pytest.fixture
    def mock_post(self):
        return post.Post(asset("basic.toml"))

    @pytest.fixture
    def mock_basic_post_results(self):
        basic = {
            "meta": {"title": "Document title",
                     "creation_date": datetime.datetime(2024, 9, 22, 10, 27)},  # noqa: DTZ001
            "content": {"markdown": "Example text.\n"},
        }
        return basic

    @pytest.fixture
    def mock_markdown_content(self):
        content_markdown = (
            "<p>Markdown is a <strong>lightweight markup language</strong> "
            "used to format plain text. It's simple to use and can be "
            "converted to HTML or other formats. Below are some key "
            "features of markdown:</p>\n<h3>1. Headers</h3>\n<p>You can "
            "create headers by using the <code>#</code> symbol:\n- "
            "<code>#</code> for a main header (H1)\n- <code>##</code> for "
            "a subheader (H2)\n- <code>###</code> for a smaller header "
            "(H3), and so on.</p>\n<p>Example:\n```markdown</p>\n<h1>This "
            "is an H1</h1>\n<h2>This is an H2</h2>"
        )
        return content_markdown

    def test_reader(self, mock_post, mock_basic_post_results):
        """Read the post's toml file and generate the post object."""
        assert mock_post.reader(mock_post.post_path) == mock_basic_post_results

    def test_basic_post(self, mock_post, mock_basic_post_results):
        """A basic post has the title, the creation date, and the content."""
        attributes = {
            "id": "161b7313299edeaa9a130fea6021382f",
            "title": "Document title",
            "creation_date": datetime.datetime(2024, 9, 22, 10, 27),  # noqa: DTZ001
            "last_update": datetime.datetime(2024, 9, 22, 10, 27),  # noqa: DTZ001
            "raw_content": mock_basic_post_results["content"],
            "author": None,
            "authors": None,
            "category": None,
            "tags": None,
            "keywords": None,
            "slug": "document-title",
            "summary": None,
            "status": None,
            "path": None,
            "filename": "document-title",
        }
        for attr in attributes:
            assert getattr(mock_post, attr) == attributes[attr]

    def test_wrong_post_format(self):
        """Check if there's meta and content tables."""
        cases = ("wrong_meta.toml", "no_meta.toml", "wrong_content.toml", "no_content.toml")
        for case in cases:
            with pytest.raises(post.InvalidMapSectionsError):
                post.Post(asset("TestReader/" + case))

    def test_post_with_path(self):
        """A post with a path defined will be tested against the website's paths."""
        _library = library.Library(asset("basic_paths.toml"))
        _post = post.Post(asset("simple_ok_post.toml"))
        assert _post.path in _library.flat_tree

    def test_post_with_wrong_parent_path(self):
        """A post with a wrong path will trigger an exception."""
        _library = library.Library(asset("basic_paths.toml"))
        with pytest.raises(post.InvalidPostPathError):
            post.Post(asset("wrong_parent_path.toml"), website_path=_library.flat_tree)

    def test_post_content_markdown(self, mock_markdown_content):
        """Retrieve a post with markdown content."""
        _library = library.Library(asset("basic_paths.toml"))
        _post = post.Post(asset("simple_ok_post_with_markdown_content.toml"), website_path=_library.flat_tree)
        assert _post.maincontent == mock_markdown_content

    def test_post_with_slug(self):
        """The slug, if present, defines the post's filename."""
        _post = post.Post(asset("simple_ok_post.toml"))
        assert _post.filename == "document-with-slug"

    def test_post_slug_with_one_unsafe_character(self):
        """An invalid slug makes the filename fallback to the title."""
        _post = post.Post(asset("simple_post_unsafe_slug.toml"))
        assert _post.filename == "document-1"

    def test_post_no_slug(self):
        """If no slug was specified, parse the title to get one."""
        _post = post.Post(asset("basic.toml"))
        assert _post.filename == "document-title"
        assert _post.slug == "document-title"

class TestSanitize:
    def test_sanitize(self):
        assert post.sanitize(None) is None
        assert post.sanitize("") is None
        assert post.sanitize("$") is None
        assert post.sanitize(" ") is None
        assert post.sanitize("-") is None
        assert post.sanitize(post.RESERVED_AND_UNSAFE) is None
        assert post.sanitize(0) == "0"
        assert post.sanitize("a") == "a"
        assert post.sanitize("A") == "a"
        assert post.sanitize("A a") == "a-a"
        assert post.sanitize("a A") == "a-a"
        assert post.sanitize("A A") == "a-a"
        assert post.sanitize("Te$t") == "tet"
        assert post.sanitize("Te$t 2") == "tet-2"
        assert post.sanitize("2 Te$t") == "2-tet"
        assert post.sanitize("Last Test Indeed") == "last-test-indeed"
