import argparse
from typing import List, Optional
import sys

from deadcode.data_types import Args
from deadcode.utils import split_comma_separated_values


def parse_command_line_arguments(args: Optional[List[str]]) -> Args:
    if not args:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()  # Docs: https://docs.python.org/3/library/argparse.html
    parser.add_argument("paths", help="Paths where to search for python files", nargs="+")
    parser.add_argument("--exclude", help="PATHS to files not to analyse at all (comma separated values)",
                        nargs="*", action="append", default=[], type=str)
    parser.add_argument("--ignore-names", help="NAMES not to report (comma separated values)",
                        nargs="*", action="append", default=[], type=str)
    parser.add_argument("--ignore-files", help="PATHS to files not to report NAMES from (comma separated values)",
                        nargs="*", action="append", default=[], type=str)

    parsed_args = parser.parse_args(args).__dict__

    for field_name in ["exclude", "ignore_names", "ignore_files"]:
        parsed_args[field_name] = split_comma_separated_values(parsed_args.get(field_name))

    return Args(**parsed_args)
