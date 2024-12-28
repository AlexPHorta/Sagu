import argparse
import pathlib
import sys
import tomllib

from src.ssg import builder, kickstart, library, organizer, post
# from ssg import builder, kickstart, library, organizer, post


def load_settings(root):
    settings = {"website_root": root}

    try:
        with open("settings.toml", 'rb') as s:
            user_settings = tomllib.load(s)
            settings.update(user_settings)
    except:
        raise TypeError("Wrong settings file type")

    settings.update({"THEME_STATIC": pathlib.Path(
                                        root,
                                        "themes",
                                        settings["THEME"],
                                        settings["STATIC"]
                                        ).absolute()})

    return settings

def generate(paths_file = 'paths.toml', root='.'):
    root = pathlib.Path(root)
    settings = load_settings(root)
    
    lib = library.Library(pathlib.Path(root, paths_file))

    # Add the posts to library
    for p in pathlib.Path(root, 'content').iterdir():
        lib.add_post(post.Post(p))

    # Set up the builder
    theme = pathlib.Path(root, 'themes', settings["THEME"])
    build = builder.Builder(theme, settings)

    # Set up the organizer
    organize = organizer.Organizer(lib, build)
    organize.gen_output(pathlib.Path(root, 'output'))


def parse_args(args):
    """Auxiliary function to ease the testing of the parser."""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--create", action="store_true", help="Create a project with a wizard.")
    group.add_argument("-g", "--generate", action="store_true", help="Generate the website content.")
    try:
        prog_args = parser.parse_args(args)
    except SystemExit as err:
        print(repr(err))
        raise err
    else:
        return prog_args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if args.create:
        kickstart.generate_project(kickstart.get_user_settings())
    elif args.generate:
        generate()
