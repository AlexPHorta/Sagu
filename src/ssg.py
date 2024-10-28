import collections
import datetime
import hashlib
import markdown
import pathlib
import re
import tomllib

from jinja2 import Environment, FileSystemLoader, select_autoescape


TEMPLATE = 'index.jinja'

RESERVED_AND_UNSAFE = r"[&$+,/:;=?@#<>\[\]{}^%~]+"


class Post:
# Store information about the posts.

	def __init__(self, post_fs_path, website_path=None):
		"""
		Create a post instance.

		:param post_fs_path: The post's (A TOML file) file path
		:param website_map: The website map (A TOML file)
		"""

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

		self.filename = self.get_filename()
		
		self.raw_content = post_object["content"]
		self.content = self.process_content()

	def reader(self, post_path):
		"""
		Read the texts and return a post object.

		:param post_path: The path to a post file
		:return: A dictionary representing the post
		"""

		try:
			with open(post_path, "rb") as post_file:
				post = tomllib.load(post_file)
			all((post["meta"], post["content"]))
		except KeyError:
			raise KeyError("Wrong file sections.")

		return post

	def parse_post_path(self, post_path, paths=None):
		"""
		Check if the post's path is in the website map.

		:param post_path: The post path defined in the TOML file
		:param paths: The website map
		:return: The post path in the website
		"""

		if paths is not None:
			if post_path in paths:
				return post_path
			else:
				raise KeyError
		else:
			return post_path

	def get_filename(self):
		slug = sanitize(self.slug)
		title = sanitize(self.title)
		return slug or title

	def process_content(self):
		final_content = ""
		for content_type, contents in self.raw_content.items():
			if content_type == 'markdown':
				final_content += markdown.markdown(contents)
		return final_content

	def get_contents(self):
		return self.__dict__

def sanitize(to_filename):
	reserved_unsafe = re.compile(RESERVED_AND_UNSAFE)
	contains_readable_characters = re.compile(r"[A-Za-z0-9]+")
	filename = None
	if to_filename is not None:
		fn = str(to_filename)
		fn = fn.replace(' ', '-').lower()
		fn = re.sub(reserved_unsafe, '', fn)
		if len(fn) > 0 and re.search(contains_readable_characters, fn):
			filename = fn
	return filename


class Library:
# Store information about the website structure and the posts.

	def __init__(self, paths_configuration=None):
		self.size = 0
		
		self.tree = self.load_paths(paths_configuration)
		self.flat_tree = self.flatten(self.tree) if paths_configuration is not None else None

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
		"""
		Add a post to the website structure

		:param the_post: The post instance
		"""

		if the_post.path in self.flat_tree:
			self.flat_tree[the_post.path].update({the_post.id: the_post}) 
			self.size += 1

	def get_post(self, post_id):
		"""
		Return a post's information to be processed.

		:param post_id: The id of the post (A string)
		"""
		post = self.find_key_nonrecursive(self.flat_tree, post_id)
		return post

	# https://stackoverflow.com/a/2524202
	def find_key_nonrecursive(self, a_dict, key):
		"""Find a key in a nested dictionary."""
		stack = [a_dict]
		while stack:
			d = stack.pop()
			if key in d:
				return d[key]
			for k, v in d.items():
				if isinstance(v, dict):
					stack.append(v)


class Builder:
# Make the html files.

	def __init__(self, templates_dir):
		self.env = Environment(loader=FileSystemLoader(templates_dir), 
								keep_trailing_newline=True)
		self.template = self.env.get_template(TEMPLATE)


class Organizer:
# Make the output folder, with the website's structure folders and respective 
# html files inside.

	def __init__(self, library, builder):
		self._library = library
		self._builder = builder

	def gen_output(self, destination): # the output directory

		for k, i in self._library.flat_tree.items():
			p = pathlib.PurePath(destination, *k.split(':'))
			pathlib.Path(str(p)).mkdir(parents=True)

			for id_, post in i.items():
				# generate the html
				post = self._library.get_post(id_)
				filename = post.filename + ".html"
				post_html = self._builder.template.render(post.get_contents())
				pathlib.Path(str(p), filename).write_text(post_html) # TODO: remove magic string
