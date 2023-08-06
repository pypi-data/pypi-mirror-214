from subprocess import PIPE, Popen
from unittest import TestCase
from unittest.mock import patch

from deadcode.cli import main
from deadcode.actions.argument_parsing import parse_command_line_arguments


class FindDeadCodeTests(TestCase):
    @patch("deadcode.cli.sys")
    def test_run_dead_code_finder_with_a_subprocess_in_a_right_directory_main(self, sys_mock):
        unused_names = main(["tests/test_case1"])
        self.assertEqual(
            unused_names,
            {
                "ANOTHER_GLOBAL_VARIABLE": "tests/test_case1/hello_world.py:4",
                "AnotherUnusedClass": "tests/test_case1/hello_world.py:19",
                "UNUSED_VARIABLE": "tests/test_case1/subdir/another_subdir/__init__.py:1",
                "another_unused_function": "tests/test_case1/subdir/one_more_file.py:1",
                "unused_global_variable": "tests/test_case1/hello_world.py:3",
            },
        )
        sys_mock.exit.assert_called_once_with(1)

    ## TODO: Add test for . path
    # def test_using_dot_to_find_files_recursively(self):
    #     unused_names = main([".", "--exclude=tests,venv"])

    #     self.assertEqual(
    #         unused_names, {
    #             'not_used_function': './tests/module_a.py:5',
    #             'FindDeadCodeTests': './tests/test_deadcode.py:7',
    #             # "ANOTHER_GLOBAL_VARIABLE": "tests/test_case1/hello_world.py:4",
    #             # "AnotherUnusedClass": "tests/test_case1/hello_world.py:19",
    #             # "UNUSED_VARIABLE": "tests/test_case1/subdir/another_subdir/__init__.py:1",
    #             # "another_unused_function": "tests/test_case1/subdir/one_more_file.py:1",
    #             # "unused_global_variable": "tests/test_case1/hello_world.py:3",
    #         },
    #     )


class CommandLineArgParsingTests(TestCase):
    def test_calling_with_one_paths_argument(self):
        args = parse_command_line_arguments(["."])
        self.assertEqual(args.paths, ["."])
        self.assertEqual(args.exclude, [])
        self.assertEqual(args.ignore_names, [])
        self.assertEqual(args.ignore_files, [])

    def test_calling_with_several_paths_argument(self):
        args = parse_command_line_arguments([".", "tests"])
        self.assertEqual(args.paths, [".", "tests"])
        self.assertEqual(args.exclude, [])
        self.assertEqual(args.ignore_names, [])
        self.assertEqual(args.ignore_files, [])

    def test_calling_with_exclude(self):
        args = parse_command_line_arguments([".", "--exclude=tests,venv"])
        self.assertEqual(args.paths, ["."])
        self.assertEqual(args.exclude, ["tests", "venv"])
        self.assertEqual(args.ignore_names, [])
        self.assertEqual(args.ignore_files, [])

    def test_calling_with_several_exclude_options(self):
        args = parse_command_line_arguments([".", "--exclude=tests,venv", "--exclude=migrations"])
        self.assertEqual(args.paths, ["."])
        self.assertEqual(args.exclude, ["tests", "venv", "migrations"])
        self.assertEqual(args.ignore_names, [])
        self.assertEqual(args.ignore_files, [])

    def test_ignore_names_and_ignore_files_command_line_argument_parsing(self):
        args = parse_command_line_arguments([".", "--ignore-files=tests,venv", "--ignore-names=BaseTestCase,lambda_handler"])
        self.assertEqual(args.paths, ["."])
        self.assertEqual(args.exclude, [])
        self.assertEqual(args.ignore_names, ["BaseTestCase", "lambda_handler"])
        self.assertEqual(args.ignore_files, ["tests", "venv"])
