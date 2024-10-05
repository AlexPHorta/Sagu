import datetime
import os.path
import unittest
import unittest.mock as mock
import uuid

from .assets import results

from src import ssg

assets = "tests/assets"


class TestReader(unittest.TestCase):

	def test_reader(self):
		self.assertEqual(ssg.reader(os.path.join(assets, "basic.toml")), 
			results.basic)

	def test_wrong_post_format(self):
		"""Check if there's meta and content tables."""
		with self.assertRaises(KeyError):
			ssg.reader(os.path.join(assets, "TestReader/wrong_meta.toml"))
			ssg.reader(os.path.join(assets, "TestReader/no_meta.toml"))
		with self.assertRaises(KeyError):
			ssg.reader(os.path.join(assets, "TestReader/wrong_content.toml"))
			ssg.reader(os.path.join(assets, "TestReader/no_content.toml"))


class TestPost(unittest.TestCase):

	def test_basic_post(self):
		basic_post = ssg.reader(os.path.join(assets, "basic.toml"))
		post_instance = ssg.Post(basic_post)
		p_i_attrs = {"id": '161b7313299edeaa9a130fea6021382f', "title": "Document title", 
			"creation_date": datetime.datetime(2024, 9, 22, 10, 27), 
			"last_update": datetime.datetime(2024, 9, 22, 10, 27),
			"raw_content": results.basic["content"], "author": None, "authors": None,
			"category": None, "tags": None, "keywords": None, "slug": None, 
			"summary": None, "status": None, "path": None}
		for attr in p_i_attrs:
			self.assertEqual(getattr(post_instance, attr), p_i_attrs[attr])

	def test_post_with_path(self):
		post1 = ssg.reader(os.path.join(assets, "post1.toml"))
		post2 = ssg.reader(os.path.join(assets, "post2.toml"))
		self.assertEqual(post1.path, ("about", "applications"))
		self.assertEqual(post2.path, ("about", "getting_started"))


class TestPostsCollection(unittest.TestCase):

	def test_empty_posts_collection(self):
		posts = ssg.PostsCollection()
		self.assertEqual(posts.size, 0)
		self.assertEqual(posts.tree, None)

	def test_empty_posts_collection_with_paths(self):
		paths = ssg.PostsCollection(os.path.join(assets, "TestPostsCollection/paths.toml"))
		self.assertEqual(paths.tree, results.test_paths)

	def test_posts_collection_with_path_and_posts(self):
		paths = ssg.PostsCollection(os.path.join(assets, "TestPostsCollection/basic_paths.toml"))
		self.assertEqual(paths.tree, results.test_basic_paths)


if __name__ == '__main__':
    unittest.main()
