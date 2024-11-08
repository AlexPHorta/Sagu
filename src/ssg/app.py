import argparse
import sys

GREETING = """Bento's static site generator!

Answer the following questions to create the necessary files.
"""

DEFAULT_SETTINGS = {
    "main_directory": ".",
    "website_title": "Default Project",
    "website_author": "",
    "website_language": "en",
    "website_url": "",
    "website_timezone": "Europe/Rome",
}

user_settings = {}

def generate_project(destination_folder, project_settings):
    ...

def get_user_settings():
    user_settings = DEFAULT_SETTINGS.copy()
    print(GREETING)  # noqa: T201

    md = get_input(
                prompt=f"> Where do you want to create your website? [Default: '{DEFAULT_SETTINGS["main_directory"]}'] "
    )
    if md != "":
        user_settings["main_directory"] = md

    wt = get_input(
                prompt=f"> What's the website's title? [Default: '{DEFAULT_SETTINGS["website_title"]}'] "
    )
    if md != "":
        user_settings["website_title"] = wt

    user_settings["website_author"] = get_input(prompt="> What's the author's name? ")

    dl = get_input(
        prompt=f"> What's the default language of the website? [Default: {DEFAULT_SETTINGS["website_language"]}]"
    )
    if dl != "":
        user_settings["website_language"] = dl

    user_settings["website_url"] = get_input(
        prompt="> What will be the website's URL " "(e.g. https://example.com)? [Default: empty]"
    )

    tz = get_input(prompt=f"> What's your timezone? [Default: {DEFAULT_SETTINGS["website_timezone"]}]")
    if tz != "":
        user_settings["website_timezone"] = tz

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
