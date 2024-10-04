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


if __name__ == '__main__':
    unittest.main()
