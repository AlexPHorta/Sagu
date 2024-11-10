import argparse
import pathlib
import sys

GREETING = """Bento's static site generator!

Answer the following questions to create the necessary files.
"""

DEFAULT_SETTINGS = [
    [["main_directory", "."], f"> Where do you want to create your website? "],
    [["website_title", "Default Project"], f"> What's the website's title? "],
    [["website_author", ""], f"> What's the author's name? "],
    [["website_language", "en"], f"> What's the default language of the website? "],
    [["website_url", ""], f"> What will be the website's URL " "(e.g. https://example.com)? "],
    [["website_timezone", "Europe/Rome"], f"> What's your timezone? "],
]


def generate_project(project_settings):
    settings = project_settings
    project_dir = ''.join(settings["website_title"].lower().split(' '))
    if settings["main_directory"] == ".":
        dest = pathlib.Path(pathlib.Path.cwd(), project_dir)
    else:
        dest = pathlib.Path(pathlib.Path.cwd(), settings["main_directory"], project_dir)
    dest.mkdir(parents=True)


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
    return input(prompt) if user_input is None else str(user_input)

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", help="Create a project with a wizard.")
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if args.create:
        user_settings = get_user_settings()
