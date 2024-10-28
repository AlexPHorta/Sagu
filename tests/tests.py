import datetime
import filecmp
import html
import pathlib
import unittest
import unittest.mock as mock
import uuid

from .assets import results
from .utils_for_testing import asset, equal_dirs, temporary_folder

from src import ssg


class TestBuilder(unittest.TestCase):

    def test_builder(self):
        """The builder will manage the mixing of posts and templates."""
        builder = ssg.Builder(asset("TestBuilder/"))
        template = builder.env.get_template("basic.jinja")
        self.assertEqual(template.render(name="Test"), "Hello, Test!\n")

    def test_builder_autoescape_off(self):
        """The builder will have autoescape turned off by default."""
        builder = ssg.Builder(asset("TestBuilder/"))
        self.assertFalse(builder.env.autoescape)

    def test_builder_build_post(self):
        library = ssg.Library(asset("basic_paths.toml"))
        post = ssg.Post(asset("TestBuilder/index.toml"), 
                        website_path=library.flat_tree)
        library.add_post(post)
        builder = ssg.Builder(asset("TestBuilder/"))
        template = builder.env.get_template("index.jinja")
        with open(asset("TestBuilder/index.html")) as f:
            test_builder_post = library.get_post(post.id)
            self.assertEqual(template.render(test_builder_post.get_contents()), 
                             f.read())

class TestOrganizer(unittest.TestCase):

    def setUp(self):
        post1 = ssg.Post(asset("simple_ok_post.toml"))
        post2 = ssg.Post(asset("simple_ok_alternative_post.toml"))
        self.library = ssg.Library(asset("basic_paths.toml"))
        self.library.add_post(post1)
        self.library.add_post(post2)
        self.builder = ssg.Builder(asset("TestBuilder/"))
        self.template = self.builder.env.get_template("index.jinja")
        self.organizer = ssg.Organizer(self.library, self.builder)

    def test_organizer(self):
        self.assertEqual(self.organizer.library, self.library)
        self.assertEqual(self.organizer.builder, self.builder)

    def test_organizer_gen_output(self):
        # Filenames follow the title when no slug specified.
        ignores = ['index.jinja', 'index.toml']
        with temporary_folder() as temp:
            self.organizer.gen_output(temp)
            compare = filecmp.dircmp(temp, asset("TestOrganizer"), ignore=ignores)
            self.assertTrue(equal_dirs(compare))
