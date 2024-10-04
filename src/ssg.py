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
		self.title = post_object["meta"]["title"]
		self.creation_date = post_object["meta"]["creation_date"]
		self.raw_content = post_object["content"]
