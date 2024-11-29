import argparse
import sys

from src.ssg import kickstart


def parse_args(args):
    """Auxiliary function to ease the testing of the parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", help="Create a project with a wizard.")
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if args.create:
        kickstart.generate_project(kickstart.get_user_settings())
