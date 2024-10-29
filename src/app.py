import argparse
import sys


GREETING = """Bento's static site generator!

Answer the following questions to create the necessary files.
"""

DEFAULT_SETTINGS = ['.', ]

def create_project():
    print(GREETING)
    answers = []

    if f:=input("> Where do you want to create your website? "
        "[Default: This same folder (.)] ") == '':
        answers.append('.')
    else:
        answers.append(f)

    answers.append(input("> What's the website's title? "))


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", 
        help="Create a project with a wizard.")
    return parser.parse_args(args)


if __name__ == "__main__":
    
    args = parse_args(sys.argv[1:])

    if args.create:
        create_project()
