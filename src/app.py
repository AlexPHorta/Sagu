import argparse
import sys

GREETING = """Bento's static site generator!

Answer the following questions to create the necessary files.
"""


def create_project():
    print(GREETING)  # noqa: T201

    default_settings = {
        "main_directory": ".",
        "website_title": "",
        "website_author": "",
        "website_language": "en",
        "website_url": "",
        "website_timezone": "Europe/Rome",
    }

    if (
        f := input(f"> Where do you want to create your website? [Default: '{default_settings["main_directory"]}'] ")
        != ""
    ):
        default_settings["main_directory"] = f

    default_settings["website_title"] = input("> What's the website's title? ")
    default_settings["website_author"] = input("> What's the author's name? ")

    if (
        f := input(f"> What's the default language of the website? [Default: {default_settings["website_language"]}]")
        == ""
    ):
        default_settings["website_language"] = f

    default_settings["website_url"] = input(
        "> What will be the website's URL " "(e.g. https://example.com)? [Default: empty]"
    )

    if f := input(f"> What's your timezone? [Default: {default_settings["website_timezone"]}]") == "":
        default_settings["website_timezone"] = f

    return default_settings


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", help="Create a project with a wizard.")
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if args.create:
        create_project()
