import argparse
import pathlib
import shutil
import sys

import tomli_w

RESOURCES = pathlib.Path(pathlib.Path(__file__).parent, "resources")

GREETING = """Bento's static site generator!

Answer the following questions to create the necessary files.
"""

DEFAULT_SETTINGS = [
    [["main_directory", "."], "> Where do you want to create your website? "],
    [["SITENAME", "Default Project"], "> What's the website's title? "],
    [["SITEAUTHOR", ""], "> What's the author's name? "],
    [["SITELANGUAGE", "en"], "> What's the default language of the website? "],
    [["SITEURL", ""], "> What will be the website's URL " "(e.g. https://example.com)? "],
    [["SITETIMEZONE", "Europe/Rome"], "> What's your timezone? "],
]


def generate_project(project_settings):
    _project_settings = project_settings
    paths = pathlib.Path(RESOURCES, "template_paths.toml").resolve()
    settings = pathlib.Path(RESOURCES, "template_settings.toml").resolve()

    # Make the project's folder
    project_dir = "".join(_project_settings["SITENAME"].lower().split(" "))
    dest = pathlib.Path(pathlib.Path.cwd(), _project_settings["main_directory"], project_dir)
    dest.mkdir(parents=True)

    # Create the inside folders
    pathlib.Path(dest, "content").mkdir()
    pathlib.Path(dest, "output").mkdir()
    pathlib.Path(dest, "templates").mkdir()

    # Copy the path file
    shutil.copyfile(paths, pathlib.Path(dest, "paths.toml"))

    #Build and copy the settings file
    with open(pathlib.Path(dest, "settings.toml"), "wb") as s:
        del _project_settings['main_directory']
        tomli_w.dump(_project_settings, s)


def get_user_settings():
    user_settings = {}
    print(GREETING)  # noqa: T201

    for setting in DEFAULT_SETTINGS:
        key = setting[0][0]
        default = setting[0][1]
        user_choice = get_input(prompt=f"{setting[1]} [Default: '{default}'] ")
        if user_choice != "":
            user_settings.update({key: user_choice})
        else:
            user_settings.update({key: default})

    return user_settings


def get_input(user_input=None, prompt=None):
    """Auxiliary function to ease the testing of prompts"""
    return input(prompt) if user_input is None else str(user_input)


def parse_args(args):
    """Auxiliary function to ease the testing of the parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", help="Create a project with a wizard.")
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if args.create:
        generate_project(get_user_settings())
