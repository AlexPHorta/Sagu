import datetime
import tomllib


def reader(post_path):
	"""Read the texts and return a post object."""

	try:
		with open(post_path, "rb") as post_file:
			data = tomllib.load(post_file)
		all((data["meta"], data["content"]))
	except KeyError:
		raise KeyError("Wrong file format.")

	return data
