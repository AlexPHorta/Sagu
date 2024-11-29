import collections

import tomllib


class Library:
    """Store information about the website structure and the posts."""

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
    def flatten(self, dictionary, parent_key=False, separator=":"):  # noqa: FBT002
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
        return self.find_key_nonrecursive(self.flat_tree, post_id)

    # https://stackoverflow.com/a/2524202
    def find_key_nonrecursive(self, a_dict, key):
        """Find a key in a nested dictionary."""
        stack = [a_dict]
        while stack:
            d = stack.pop()
            if key in d:
                return d[key]
            for v in d.values():
                if isinstance(v, dict):
                    stack.append(v)  # noqa: PERF401
        return
