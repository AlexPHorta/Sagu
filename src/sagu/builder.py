import pathlib

from jinja2 import Environment, FileSystemLoader


class Builder:
    # Make the html files.

    def __init__(self, templates_dir, website_settings):
        self.settings = website_settings
        self.env = Environment(loader=FileSystemLoader(templates_dir),
                               autoescape=True,
                               keep_trailing_newline=True)
        self.template = self.env.get_template(
                self.settings["BASETEMPLATE"], globals=self.settings)
