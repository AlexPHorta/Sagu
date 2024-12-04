import argparse
import sys

from src.ssg import kickstart


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
