import datetime
import tomllib


def reader(file_path):

	try:
		with open(file_path, "rb") as post_file:
			data = tomllib.load(post_file)
		data["meta"]
	except KeyError:
		raise KeyError("Wrong file format.")

	return data
