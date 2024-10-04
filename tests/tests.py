import datetime
import os.path
import unittest

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
			ssg.reader(os.path.join(assets, "wrong_meta.toml"))
			ssg.reader(os.path.join(assets, "no_meta.toml"))
		with self.assertRaises(KeyError):
			ssg.reader(os.path.join(assets, "no_content.toml"))
			ssg.reader(os.path.join(assets, "wrong_content.toml"))


class TestPost(unittest.TestCase):

	def test_basic_post(self):
		basic_post = ssg.reader(os.path.join(assets, "basic.toml"))
		post_instance = ssg.Post(basic_post)
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


if __name__ == '__main__':
    unittest.main()
