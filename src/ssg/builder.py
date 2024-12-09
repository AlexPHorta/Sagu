from jinja2 import Environment, FileSystemLoader

TEMPLATE = "index.jinja"


class Builder:
    # Make the html files.

    def __init__(self, templates_dir):
        self.env = Environment(loader=FileSystemLoader(templates_dir),
                               autoescape=True,
                               keep_trailing_newline=True)
        self.template = self.env.get_template(TEMPLATE)
