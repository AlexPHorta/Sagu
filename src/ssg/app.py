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
    user_settings = DEFAULT_SETTINGS.copy()
    print(GREETING)  # noqa: T201

    if (
        md := get_input(prompt=f"> Where do you want to create your website? [Default: '{DEFAULT_SETTINGS["main_directory"]}'] ")
        != ""
    ):
        user_settings["main_directory"] = md

    user_settings["website_title"] = get_input(prompt="> What's the website's title? ")
    user_settings["website_author"] = get_input(prompt="> What's the author's name? ")

    if (
        dl := get_input(prompt=f"> What's the default language of the website? [Default: {DEFAULT_SETTINGS["website_language"]}]")
        == ""
    ):
        user_settings["website_language"] = dl

    user_settings["website_url"] = get_input(
        prompt="> What will be the website's URL " "(e.g. https://example.com)? [Default: empty]"
    )

    if tz := get_input(prompt=f"> What's your timezone? [Default: {DEFAULT_SETTINGS["website_timezone"]}]") == "":
        user_settings["website_timezone"] = tz

    return user_settings

def get_input(user_input=None, prompt=None):
    if user_input is None:
        return input(prompt)
    else:
        return user_input


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", help="Create a project with a wizard.")
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if args.create:
        create_project()
