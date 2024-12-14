import hashlib
import re

import markdown
import tomllib

TEMPLATE = "index.jinja"

RESERVED_AND_UNSAFE = r"[&$+,/:;=?@#<>\[\]{}^%~]+"


class InvalidMapSectionsError(Exception):
    def __init__(self):
        super().__init__("Invalid sections in website map file")


class Post:
    """Store information about the posts."""

    def __init__(self, post_fs_path, website_path=None):
        """
        Create a post instance.

        :param post_fs_path: The post's (A TOML file) file path
        :param website_map: The website map (A TOML file)
        """

        self.post_path = post_fs_path
        post_object = self.reader(self.post_path)
        m = post_object["meta"]

        self.title = m["title"]
        self.creation_date = m["creation_date"]
        self.last_update = m["creation_date"]

        self.id = hashlib.md5(
            bytes(f"{self.title}{self.creation_date.isoformat()}", encoding="utf-8"), usedforsecurity=False
        ).hexdigest()

        self.author = m.get("author")
        self.authors = m.get("authors")
        self.category = m.get("category")
        self.tags = m.get("tags")
        self.keywords = m.get("keywords")
        self.slug = m.get("slug")
        self.summary = m.get("summary")
        self.status = m.get("status")

        post_url_path = m.get("path")
        self.path = post_url_path if post_url_path is None else self.parse_post_path(post_url_path, paths=website_path)

        self.filename = self.get_filename()

        self.raw_content = post_object["content"]
        self.maincontent = self.process_content()

    def reader(self, post_path):
        """
        Read the texts and return a post object.

        :param post_path: The path to a post file
        :return: A dictionary representing the post
        """

        try:
            with open(post_path, "rb") as post_file:
                post = tomllib.load(post_file)
            all((post["meta"], post["content"]))
        except KeyError as err:
            raise InvalidMapSectionsError from err

        return post

    def parse_post_path(self, post_path, paths=None):
        """
        Check if the post's path is in the website map.

        :param post_path: The post path defined in the TOML file
        :param paths: The website map
        :return: The post path in the website
        """

        if paths is not None:
            if post_path in paths:
                return post_path
            else:  # noqa: RET505
                raise KeyError
        else:
            return post_path

    def get_filename(self):
        """Return the filename for the post"""
        slug = sanitize(self.slug)
        title = sanitize(self.title)
        return slug or title

    def process_content(self):
        """Convert the post content to markdown"""
        final_content = ""
        for content_type, contents in self.raw_content.items():
            if content_type == "markdown":
                final_content += markdown.markdown(contents)
        return final_content

    def get_contents(self):
        return self.__dict__


def sanitize(to_filename):
    """Auxiliary function to sanitize the titles and slugs provided in the post file"""
    reserved_unsafe = re.compile(RESERVED_AND_UNSAFE)
    contains_readable_characters = re.compile(r"[A-Za-z0-9]+")
    filename = None
    if to_filename is not None:
        fn = str(to_filename)
        fn = fn.replace(" ", "-").lower()
        fn = re.sub(reserved_unsafe, "", fn)
        if len(fn) > 0 and re.search(contains_readable_characters, fn):
            filename = fn
    return filename
