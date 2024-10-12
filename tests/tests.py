import datetime
import os.path
import unittest
import unittest.mock as mock
import uuid

from .assets import results

from src import ssg

assets = "tests/assets"

def asset(asset_name):
	assets = "tests/assets"
	return os.path.join(assets, asset_name)


class TestPost(unittest.TestCase):

	def test_reader(self):
		"""Read the post's toml file and generate the post object."""
		post = ssg.Post(asset("basic.toml"))
		self.assertEqual(post.reader(post.post_path), 
			results.basic)

	def test_wrong_post_format(self):
		"""Check if there's meta and content tables."""
		with self.assertRaises(KeyError):
			cases = ('wrong_meta.toml', 'no_meta.toml', 'wrong_content.toml', 
					 'no_content.toml')
			for case in cases:
				ssg.Post(asset("TestReader/" + case))


	def test_basic_post(self):
		"""A basic post has the title, the creation date, and the content."""
		post_instance = ssg.Post(asset("basic.toml"))
		attributes = {"id": '161b7313299edeaa9a130fea6021382f', "title": "Document title", 
			"creation_date": datetime.datetime(2024, 9, 22, 10, 27), 
			"last_update": datetime.datetime(2024, 9, 22, 10, 27),
			"raw_content": results.basic["content"], "author": None, "authors": None,
			"category": None, "tags": None, "keywords": None, "slug": None, 
			"summary": None, "status": None, "path": None}
		for attr in attributes:
			self.assertEqual(getattr(post_instance, attr), attributes[attr])

	def test_post_with_path(self):
		"""A post with a path defined will be tested against the website's paths."""
		paths = ssg.PostLibrary(asset("basic_paths.toml"))
		post1 = ssg.Post(asset("simple_ok_post.toml"))
		self.assertTrue(post1.path in paths.flat_tree)

	def test_post_with_wrong_parent_path(self):
		"""A post with a wrong path will trigger an exception."""
		paths = ssg.PostLibrary(asset("basic_paths.toml"))
		with self.assertRaises(KeyError):
			ssg.Post(asset("wrong_parent_path.toml"), website_path=paths.flat_tree)


class TestPostLibrary(unittest.TestCase):

	def test_empty_posts_collection(self):
		"""The collection of posts."""
		posts = ssg.PostLibrary()
		self.assertEqual(posts.size, 0)
		self.assertEqual(posts.flat_tree, None)

	def test_empty_posts_collection_with_path(self):
		"""The website map is defined in a toml file."""
		paths = ssg.PostLibrary(asset("TestPostLibrary/paths.toml"))
		self.assertEqual(paths.flat_tree, results.test_flat_paths)

	def test_posts_collection_with_path_and_posts(self):
		"""Posts added to the collection will be tested against the paths when added."""
		posts = ssg.PostLibrary(asset("basic_paths.toml"))

		post1 = ssg.Post(asset("simple_ok_post.toml"), website_path=posts.flat_tree)
		posts.add_post(post1)
		self.assertEqual(posts.size, 1)
		self.assertEqual(posts.flat_tree['about:applications'], 
						 {'073032467b1bffb192b560d04f9b0192': post1})

		post2 = ssg.Post(asset("simple_ok_alternative_post.toml"), 
								website_path=posts.flat_tree)
		posts.add_post(post2)
		self.assertEqual(posts.size, 2)
		self.assertEqual(posts.flat_tree['about:getting_started'], 
						 {'87ce9d57e6f1a53a887e4834b9d620e0': post2})

	def test_posts_retrieve_post_content(self):
		posts = ssg.PostLibrary(asset("basic_paths.toml"))
		post = ssg.Post(asset("simple_ok_post.toml"), website_path=posts.flat_tree)
		posts.add_post(post)
		self.assertEqual(posts.get_post(post.id), {'id':post.id, 'title':post.title, 
				'content':post.raw_content['markdown'].strip()})


class TestBuilder(unittest.TestCase):

	def test_builder(self):
		builder = ssg.Builder(asset("TestBuilder/"))
		template = builder.env.get_template("basic.jinja")
		self.assertEqual(template.render(name="Test"), "Hello, Test!")

	def test_builder_autoescape_on(self):
		builder = ssg.Builder(asset("TestBuilder/"))
		self.assertTrue(builder.env.autoescape)

	def test_builder_build_post(self):
		posts = ssg.PostLibrary(asset("TestBuilder/basic_paths.toml"))
		post = ssg.Post(asset("TestBuilder/index.toml"), 
						website_path=posts.flat_tree)
		posts.add_post(post)
		builder = ssg.Builder(asset("TestBuilder/"))
		template = builder.env.get_template("index.jinja")
		self.assertEqual(template.render(posts.get_post(post.id)), 
						 '<!doctype html>\n<html>\n\n<head>\n  <meta charset="ut'
						 'f-8">\n  <meta name="viewport" content="width=device-w'
						 'idth, initial-scale=1">\n  <title>Document 1</title>\n'
						 '</head>\n\n<body>\n\n  <!-- Add your site or applicati'
						 'on content here -->\n  <h1>Document 1</h1>\n  <p>Examp'
						 'le 1.</p>\n\n</body>\n\n</html>')


if __name__ == '__main__':
	unittest.main()
