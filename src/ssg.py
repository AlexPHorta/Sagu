import datetime
import hashlib
import tomllib



def reader(post_path):
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


class Post:

	def __init__(self, post_object):
		"""Create a post instance.

		Arguments:
		post_object - a dictionary"""
		m = post_object["meta"]
		self.title = m["title"]
		self.creation_date = m["creation_date"]
		self.id = hashlib.md5(bytes(f"{self.title}{self.creation_date.isoformat()}",
			encoding="utf-8"), usedforsecurity=False).hexdigest()
		self.last_update = m["creation_date"]
		self.author = m.get("author")
		self.authors = m.get("authors")
		self.category = m.get("category")
		self.tags = m.get("tags")
		self.keywords = m.get("keywords")
		self.slug = m.get("slug")
		self.summary = m.get("summary")
		self.status = m.get("status")
		self.path = m.get("path")
		self.raw_content = post_object["content"]


class PostsCollection:

	def __init__(self, paths_configuration=None):
		self.size = 0
		self.tree = self.load_paths(paths_configuration)

	def load_paths(self, paths):

		if paths is None:
			return []

		with open(paths, "rb") as paths_file:
			paths = tomllib.load(paths_file)

		return paths
