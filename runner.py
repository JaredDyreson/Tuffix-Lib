#!/usr/bin/env python3.9

# from Tuffix.Driver import *
# from Tuffix.Configuration import DEFAULT_BUILD_CONFIG
# from Tuffix.Keywords import KeywordContainer
# from Tuffix.Exceptions import *
# from Tuffix.Quieter import quiet
# from UnitTests.SequentialTest import SequentialTestLoader

import unittest
import importlib.util
import os
import pathlib

"""
format:

"<CLASS NAME OF TEST>": ["PATH", SILENT(False)/VERBOSE(True)]
"""

runner = unittest.TextTestRunner()


def construct_filesystem(pedantic: bool) -> list[dict]:
    if not(isinstance(pedantic, bool)):
        raise ValueError(f'{pedantic=} is not a `bool`')

    excluded_dirs = ["__pycache__", "TEST"]
    excluded_files = ["SequentialTest.py", "__init__.py"]
    container = []

    for dirpath, dirs, filepath in os.walk("UnitTests", topdown=True):
        dirs.sort()
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        filepath[:] = [f for f in filepath if f not in excluded_files]
        test_name = os.path.basename(dirpath)
        if not(test_name == "UnitTests"):
            filepath = [(path, pedantic) for path in filepath]
            container.append(
                {test_name: filepath}
            )
    return container


def conduct_test(path: pathlib.Path, pedantic: bool):
    if not(isinstance(path, pathlib.Path) and
           isinstance(pedantic, bool)):
        raise ValueError(f'{path=} is not a `pathlib.Path`')

    spec = importlib.util.spec_from_file_location("test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _test = getattr(module, name, None)
    test_suite = SequentialTestLoader().loadTestsFromTestCase(_test)
    if(pedantic):
        runner.run(test_suite)
    else:
        with quiet():
            runner.run(test_suite)


def run_tests():
    tests = construct_filesystem(pedantic=False)
    base_folder = pathlib.Path("UnitTests")
    for test in tests:
        for name, arguments in test.items():
            for subtest, pedantic in arguments:
                path = (base_folder / name / subtest)
                conduct_test(path, pedantic)


run_tests()
