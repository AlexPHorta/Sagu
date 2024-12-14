import pathlib

from jinja2 import Environment, FileSystemLoader

TEMPLATE = "index.jinja"
STATIC = "themes/sagu/static"


class Builder:
    # Make the html files.

    def __init__(self, templates_dir, website_settings):
        self.env = Environment(loader=FileSystemLoader(templates_dir),
                               autoescape=True,
                               keep_trailing_newline=True)
        self.template = self.env.get_template(
                TEMPLATE, globals={"SITENAME": "Cats and Dogs",
                                   "SITELANGUAGE": "en",
                                   "STATIC": pathlib.Path(website_settings["website_root"], STATIC).absolute()})
