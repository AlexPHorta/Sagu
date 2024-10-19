import datetime
import html
import pathlib
import unittest
import unittest.mock as mock
import uuid

from .assets import results
from utils import temporary_folder

from src import ssg


def asset(asset_name):
	assets = "tests/assets"
	return pathlib.PurePath(assets, asset_name)


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
			"slug": None, "summary": None, "status": None, "path": None}
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
		post1 = ssg.Post(asset("simple_ok_post.toml"))
		self.assertTrue(post1.path in library.flat_tree)

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


class TestLibrary(unittest.TestCase):

	def setUp(self):
		self.library = ssg.Library(asset("basic_paths.toml"))

	def test_empty_library(self):
		"""The library of posts."""
		library = ssg.Library()
		self.assertEqual(library.size, 0)
		self.assertEqual(library.flat_tree, None)

	def test_empty_library_with_path(self):
		"""The website map is defined in a toml file."""
		library = ssg.Library(asset("TestLibrary/paths.toml"))
		self.assertEqual(library.flat_tree, results.test_flat_paths)

	def test_library_with_path_and_posts(self):
		"""Posts added to the library will be tested against the paths when added."""
		library = ssg.Library(asset("basic_paths.toml"))
		cases = {"simple_ok_post.toml": ('about:applications', 
							'073032467b1bffb192b560d04f9b0192'),
				 "simple_ok_alternative_post.toml": ('about:getting_started', 
				 			'87ce9d57e6f1a53a887e4834b9d620e0')}
		for case, attrs in cases.items():
			post = ssg.Post(asset(case), website_path=library.flat_tree)
			library.add_post(post)
			self.assertEqual(library.flat_tree[attrs[0]], {attrs[1]: post})
		self.assertEqual(library.size, 2)

	def test_library_retrieve_post_content(self):
		"""The library will manage the posts, so, retrieving a post's content is the library's function."""
		library = ssg.Library(asset("basic_paths.toml"))
		post = ssg.Post(asset("simple_ok_post.toml"), website_path=library.flat_tree)
		library.add_post(post)
		self.assertEqual(library.get_post(post.id), {'id':post.id, 
						 'title':post.title, 'content':post.content})


class TestBuilder(unittest.TestCase):

	def test_builder(self):
		"""The builder will manage the mixing of posts and templates."""
		builder = ssg.Builder(asset("TestBuilder/"))
		template = builder.env.get_template("basic.jinja")
		self.assertEqual(template.render(name="Test"), "Hello, Test!")

	def test_builder_autoescape_on(self):
		"""The builder will have autoescape turned on by default."""
		builder = ssg.Builder(asset("TestBuilder/"))
		self.assertTrue(builder.env.autoescape)

	def test_builder_build_post(self):
		library = ssg.Library(asset("basic_paths.toml"))
		post = ssg.Post(asset("TestBuilder/index.toml"), 
						website_path=library.flat_tree)
		library.add_post(post)
		builder = ssg.Builder(asset("TestBuilder/"))
		template = builder.env.get_template("index.jinja")
		with open(asset("TestBuilder/index.html")) as f:
			# using html.unescape just to ease the comparison
			self.assertEqual(html.unescape(
							 template.render(library.get_post(post.id))), 
							 f.read().strip())

class TestOrganizer(unittest.TestCase):

	def setUp(self):
		self.library = ssg.Library(asset("basic_paths.toml"))
		self.organizer = ssg.Organizer(self.library)

	def test_organizer(self):
		self.assertEqual(self.organizer.origin, self.library)

	def test_organizer_make_paths(self):
		self.assertEqual(self.organizer.make_paths(), 
						 (pathlib.PurePath('about/applications'),
						  pathlib.PurePath('about/getting_started')))

	def test_organizer_gen_output(self):
		self.assertEqual(self.organizer.gen_output(), 0)


if __name__ == '__main__':
	unittest.main()
