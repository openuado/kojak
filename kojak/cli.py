import argparse
import os
import sys

from kojak.common import is_valid_path


class readable_path(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            is_valid_path(values)
        except (IOError, OSError) as err:
            print(str(err))
            parser.print_help()
            sys.exit(1)
        else:
            setattr(namespace, self.dest, values)


def argparser():
    parser = argparse.ArgumentParser(description="Analyze python file")
    parser.add_argument(
        "file",
        nargs="?",
        action=readable_path,
        help="Path to analyze. \
                        If not provided kojak analyze the current working dir",
        default=os.getcwd(),
    )
    parser.add_argument(
        "-s",
        "--summarize",
        action="store_true",
        help="If display a summary of the analyze",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Only display the kojak version number",
    )
    return parser.parse_args()
