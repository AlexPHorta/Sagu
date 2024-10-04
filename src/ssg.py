import datetime
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

