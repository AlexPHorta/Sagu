import argparse
import sys

GREETING = """Bento's static site generator!

Answer the following questions to create the necessary files.
"""

DEFAULT_SETTINGS = {
    "main_directory": ".",
    "website_title": "",
    "website_author": "",
    "website_language": "en",
    "website_url": "",
    "website_timezone": "Europe/Rome",
}

def create_project():
    print(GREETING)  # noqa: T201

    if (
        f := input(f"> Where do you want to create your website? [Default: '{DEFAULT_SETTINGS["main_directory"]}'] ")
        != ""
    ):
        DEFAULT_SETTINGS["main_directory"] = f

    DEFAULT_SETTINGS["website_title"] = input("> What's the website's title? ")
    DEFAULT_SETTINGS["website_author"] = input("> What's the author's name? ")

    if (
        f := input(f"> What's the default language of the website? [Default: {DEFAULT_SETTINGS["website_language"]}]")
        == ""
    ):
        DEFAULT_SETTINGS["website_language"] = f

    DEFAULT_SETTINGS["website_url"] = input(
        "> What will be the website's URL " "(e.g. https://example.com)? [Default: empty]"
    )

    if f := input(f"> What's your timezone? [Default: {DEFAULT_SETTINGS["website_timezone"]}]") == "":
        DEFAULT_SETTINGS["website_timezone"] = f

    return DEFAULT_SETTINGS


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", help="Create a project with a wizard.")
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if args.create:
        create_project()
