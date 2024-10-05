import datetime
import hashlib
import tomllib


class Post:

	def __init__(self, post_fs_path):
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
		self.path = post_url_path if post_url_path is None else self.parse_post_path(post_url_path)
		
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
		post_path = tuple(post_path.split(":"))

		if paths is not None:
			pass
		else:
			return post_path


class PostsCollection:

	def __init__(self, paths_configuration=None):
		self.size = 0
		self.tree = self.load_paths(paths_configuration)

	def load_paths(self, paths):

		if paths is not None:
			with open(paths, "rb") as paths_file:
				paths = tomllib.load(paths_file)

		return paths
