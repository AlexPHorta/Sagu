import collections
import datetime
import hashlib
import tomllib


class Post:

	def __init__(self, post_fs_path, website_path=None):
		"""Create a post instance.

		Arguments:
		post_object - a dictionary"""
		self.post_path = post_fs_path
		post_object = self.reader(self.post_path)
		m = post_object["meta"]
		
		self.title = m["title"]
		self.creation_date = m["creation_date"]
		self.last_update = m["creation_date"]
		
		self.id = hashlib.md5(bytes(f"{self.title}{self.creation_date.isoformat()}",
			encoding="utf-8"), usedforsecurity=False).hexdigest()
		
		self.author = m.get("author")
		self.authors = m.get("authors")
		self.category = m.get("category")
		self.tags = m.get("tags")
		self.keywords = m.get("keywords")
		self.slug = m.get("slug")
		self.summary = m.get("summary")
		self.status = m.get("status")

		post_url_path = m.get("path")
		self.path = post_url_path if post_url_path is None else self.parse_post_path(
					post_url_path, paths=website_path)
		
		self.raw_content = post_object["content"]

	def reader(self, post_path):
		"""Read the texts and return a post object.

		Arguments:
		post_path - path to a post file"""

		try:
			with open(post_path, "rb") as post_file:
				post = tomllib.load(post_file)
			all((post["meta"], post["content"]))
		except KeyError:
			raise KeyError("Wrong file sections.")

		return post

	def parse_post_path(self, post_path, paths=None):
		# post_path = tuple(post_path.split(":"))

		if paths is not None:
			if post_path in paths:
				return post_path
			else:
				raise KeyError
		else:
			return post_path


class PostsCollection:

	def __init__(self, paths_configuration=None):
		self.size = 0
		
		tree = self.load_paths(paths_configuration)
		self.flat_tree = self.flatten(tree) if paths_configuration is not None else None

	def load_paths(self, paths):

		if paths is not None:
			with open(paths, "rb") as paths_file:
				paths = tomllib.load(paths_file)

		return paths

	# Adapted from https://stackoverflow.com/a/62186053
	def flatten(self, dictionary, parent_key=False, separator=':'):
		"""
		Turn a nested dictionary into a flattened dictionary
		:param dictionary: The dictionary to flatten
		:param parent_key: The string to prepend to dictionary's keys
		:param separator: The string used to separate flattened keys
		:return: A flattened dictionary
		"""
		items = []
		for key, value in dictionary.items():
			new_key = str(parent_key) + separator + key if parent_key else key
			if isinstance(value, collections.abc.MutableMapping) and len(value) > 0:
				items.extend(self.flatten(value, new_key, separator).items())
			else:
				items.append((new_key, value))
		return dict(items)

	def add_post(self, the_post):
		if the_post.path in self.flat_tree:
			self.flat_tree[the_post.path].update({the_post.id: the_post}) 
			self.size += 1
