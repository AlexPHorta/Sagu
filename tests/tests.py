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
		self.assertEqual(post_instance.id, '161b7313299edeaa9a130fea6021382f')  # MD5 hex digest
		self.assertEqual(post_instance.title, "Document title")
		self.assertEqual(post_instance.creation_date, datetime.datetime(2024, 9, 22, 10, 27))
		self.assertEqual(post_instance.last_update, datetime.datetime(2024, 9, 22, 10, 27))
		self.assertEqual(post_instance.raw_content, results.basic["content"])
		self.assertEqual(post_instance.author, None)
		self.assertEqual(post_instance.authors, None)
		self.assertEqual(post_instance.category, None)
		self.assertEqual(post_instance.tags, None)
		self.assertEqual(post_instance.keywords, None)
		self.assertEqual(post_instance.slug, None)
		self.assertEqual(post_instance.summary, None)
		self.assertEqual(post_instance.status, None)
		self.assertEqual(post_instance.path, None)


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
