from typing import Dict, List, Optional
from collections import defaultdict
import os
import sys
import re
from fnmatch import fnmatch

from deadcode.data_types import Args, FileContent, Filename, Pathname, VariableName
from deadcode.actions.argument_parsing import parse_command_line_arguments


def does_path_match_patterns(path: Pathname, patterns: Optional[List[Pathname]]) -> bool:
    if path != "." and patterns:
        for pattern in patterns:
            if fnmatch(path, pattern):
                return True
    return False


def find_python_filenames(args: Args):
    """Recursively searches for Python filenames in provided paths."""
    python_filenames = []
    for path in args.paths:
        if does_path_match_patterns(path, args.exclude):
            continue

        if os.path.isfile(path):
            filename = path
            if os.path.splitext(filename)[1] == ".py":
                python_filenames.append(filename)
        else:
            for path, _, filenames in os.walk(path):
                if does_path_match_patterns(path, args.exclude):
                    continue

                for f in filenames:
                    filename = os.path.join(path, f)
                    if (os.path.splitext(filename)[1] == ".py" and
                        not does_path_match_patterns(filename, args.exclude)):
                        python_filenames.append(filename)

    return python_filenames


def read_files(filenames: List[Filename]) -> Dict[Filename, FileContent]:
    files = {}
    for filename in filenames:
        with open(filename, "r") as f:
            files[filename] = f.read()
    return files


def parse_global_names(
    files: Dict[Filename, FileContent], args: Args
) -> Dict[VariableName, Filename]:
    patterns = [
        r"^(\w+)\s*=",
        r"^def\s+(\w+)\s*\(?",
        r"^class\s+(\w+)\s*\(?:?",
    ]

    global_variable_names = {}
    for filename, file_content in files.items():
        if does_path_match_patterns(filename, args.ignore_files):
            continue

        for pattern in patterns:
            for line_nr, line in enumerate(file_content.split("\n"), 1):
                if global_variable_name_in_file := re.findall(pattern, line):
                    variable_name = global_variable_name_in_file[0]
                    # TODO: could find the column name and add it to the output.
                    global_variable_names[variable_name] = f"{filename}:{line_nr}"

    return global_variable_names


def remove_comments_from_file_content(file_content: str) -> str:
    # TODO: add a unit test for this feature.
    file_lines_without_comments = []
    for line in file_content:
        if "#" in line:
            # TODO: should ignore # in strings.
            line = line.split("#", 1)[0]
        file_lines_without_comments.append(line)
    return "".join(file_lines_without_comments)


def remove_comments(files: Dict[Filename, FileContent]) -> Dict[Filename, FileContent]:
    files_without_comments = {}
    for filename, file_content in files.items():
        files_without_comments[filename] = remove_comments_from_file_content(file_content)
    return files_without_comments
        

def find_unused_names(
    files: Dict[str, str], global_names: Dict[VariableName, Filename], args: Args
) -> Dict[VariableName, Filename]:
    name_occourencies = defaultdict(int)
    for name in global_names.keys():
        for file_content in files.values():
            name_occourencies[name] += file_content.count(name)

    unused_variables = {
        name: filename
        for name, filename in global_names.items()
        if name_occourencies[name] == 1 and name not in args.ignore_names
    }
    return unused_variables


def print_unused_names(unused_names: Dict[VariableName, Filename]):
    # TODO: add line number to output
    for name, filename in unused_names.items():
        print(
            filename,
            "\033[91mF851\033[0m",
            f"Global \033[1m{name}\033[0m is never used",
        )


def main(command_line_args: Optional[List[str]] = None) -> Dict[VariableName, Filename]:
    args = parse_command_line_arguments(command_line_args)

    python_filenames = find_python_filenames(args=args)
    files = read_files(python_filenames)
    files_without_comments = remove_comments(files)

    global_names = parse_global_names(files, args=args)
    unused_names = find_unused_names(files_without_comments, global_names, args=args)

    print_unused_names(unused_names)
    if unused_names:
        sys.exit(1)
    return unused_names


if __name__ == "__main__":
    main()
