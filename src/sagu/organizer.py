import pathlib


class Organizer:
    # Make the output folder, with the website's structure folders and respective
    # html files inside.

    def __init__(self, library, builder):
        self.library = library
        self.builder = builder

    def gen_output(self, destination):  # the output directory
        for k, i in self.library.flat_tree.items():
            p = pathlib.Path(destination, *k.split(":"))
            pathlib.Path(str(p)).mkdir(parents=True, exist_ok=True)

            for _post in i.values():
                # generate the html
                post = self.library.get_post_by_id(_post.id)
                filename = post.filename + ".html"
                post_html = self.builder.template.render(post.get_contents())
                pathlib.Path(str(p), filename).write_text(post_html)
