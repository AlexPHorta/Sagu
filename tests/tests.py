import datetime
import os.path
import unittest
import unittest.mock as mock
import uuid

from .assets import results

from src import ssg

assets = "tests/assets"


class TestPost(unittest.TestCase):

	def test_reader(self):
		post = ssg.Post(os.path.join(assets, "basic.toml"))
		self.assertEqual(post.reader(post.post_path), 
			results.basic)

	def test_wrong_post_format(self):
		"""Check if there's meta and content tables."""
		with self.assertRaises(KeyError):
			ssg.Post(os.path.join(assets, "TestReader/wrong_meta.toml"))
			ssg.Post(os.path.join(assets, "TestReader/no_meta.toml"))
			ssg.Post(os.path.join(assets, "TestReader/wrong_content.toml"))
			ssg.Post(os.path.join(assets, "TestReader/no_content.toml"))

	def test_basic_post(self):
		post_instance = ssg.Post(os.path.join(assets, "basic.toml"))
		p_i_attrs = {"id": '161b7313299edeaa9a130fea6021382f', "title": "Document title", 
			"creation_date": datetime.datetime(2024, 9, 22, 10, 27), 
			"last_update": datetime.datetime(2024, 9, 22, 10, 27),
			"raw_content": results.basic["content"], "author": None, "authors": None,
			"category": None, "tags": None, "keywords": None, "slug": None, 
			"summary": None, "status": None, "path": None}
		for attr in p_i_attrs:
			self.assertEqual(getattr(post_instance, attr), p_i_attrs[attr])

	def test_post_with_path(self):
		paths = ssg.PostsCollection(os.path.join(assets, "basic_paths.toml"))
		post1 = ssg.Post(os.path.join(assets, "post1.toml"))
		self.assertTrue(post1.path in paths.flat_tree)

	def test_post_with_wrong_parent_path(self):
		paths = ssg.PostsCollection(os.path.join(assets, "basic_paths.toml"))
		with self.assertRaises(KeyError):
			ssg.Post(os.path.join(assets, "post2.toml"), website_path=paths.flat_tree)


class TestPostsCollection(unittest.TestCase):

	def test_empty_posts_collection(self):
		posts = ssg.PostsCollection()
		self.assertEqual(posts.size, 0)
		self.assertEqual(posts.flat_tree, None)

	def test_empty_posts_collection_with_paths(self):
		paths = ssg.PostsCollection(os.path.join(assets, "TestPostsCollection/paths.toml"))
		self.assertEqual(paths.flat_tree, results.test_flat_paths)

	def test_posts_collection_with_path_and_posts(self):
		posts = ssg.PostsCollection(os.path.join(assets, "basic_paths.toml"))
		post1 = ssg.Post(os.path.join(assets, "post1.toml"), website_path=posts.flat_tree)
		posts.add_post(post1)
		self.assertEqual(posts.size, 1)
		self.assertEqual(posts.flat_tree['about:applications'], 
						 {'073032467b1bffb192b560d04f9b0192': post1})
		post3 = ssg.Post(os.path.join(assets, "post3.toml"), website_path=posts.flat_tree)
		posts.add_post(post3)
		self.assertEqual(posts.size, 2)
		self.assertEqual(posts.flat_tree['about:getting_started'], 
						 {'87ce9d57e6f1a53a887e4834b9d620e0': post3})



if __name__ == '__main__':
	unittest.main()
