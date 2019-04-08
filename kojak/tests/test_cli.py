# -*- encoding: utf-8 -*-
import io
import os
import sys
import tempfile
import unittest

from kojak.cli import classes
from kojak.cli import imports
from kojak.cli import is_valid_path
from kojak.cli import pluralize
from kojak.cli import summarize
from kojak.utils import Analyze
from kojak.utils import Module

from sample import sample


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.pyfile = io.StringIO(sample)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)

    def test_pluralize(self):
        self.assertEqual(pluralize(5, 'test', 'tests'), 'tests')
        self.assertEqual(pluralize("5", 'test', 'tests'), 'tests')
        self.assertEqual(pluralize([1, 2], 'test', 'tests'), 'tests')
        self.assertEqual(pluralize([1, 2], 'test'), 'tests')
        self.assertEqual(pluralize([1], 'test', 'tests'), 'test')
        self.assertEqual(pluralize([1], 'test'), 'test')
        self.assertEqual(pluralize([], 'test', 'tests'), 'test')
        with self.assertRaises(ValueError):
            self.assertEqual(pluralize("ddd5", 'test', 'tests'), 'tests')

    def test_is_valid_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = "{dir}/module.py".format(dir=tmpdir)
            fake = "{dir}/fake".format(dir=tmpdir)

            with open(module_path, "w+") as module:
                module.write("test")
            is_valid_path(module_path)

            with self.assertRaises(IOError):
                is_valid_path(fake)

            os.chmod(module_path, 222)

            with self.assertRaises(OSError):
                is_valid_path(module_path)

    def test_classes(self):
        expected_output = "This module contains 2 classes:-Bar-run-bar-Foo"
        expected_output2 = "This module contains 2 classes:-Foo-Bar-run-bar"
        captured_output = io.StringIO()
        sys.stdout = captured_output
        classes(self.module)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().replace("\t", "").replace("\n", "")
        try:
            self.assertEqual(output, expected_output)
        except AssertionError:
            # (hberaud) Python 3.5 list classes in a random order
            # so to avoid assertion errors due to the python 3.5
            # behaviour that is different from python higher versions
            # we want to check the another expected output with
            # classes in different order.
            self.assertEqual(output, expected_output2)

    def test_imports(self):
        expected_output = "This module /fake/module contains 3 "\
            "imports-Import requests-Import abc-From foo import bar"
        captured_output = io.StringIO()
        sys.stdout = captured_output
        imports(self.module)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().replace("\t", "").replace("\n", "")
        self.assertEqual(output, expected_output)

    def test_summarize(self):
        expected_output = "This project contains 1 moduleThis project "\
            "contains 3 importsThis project contains 1 classes"
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = "{dir}/module.py".format(dir=tmpdir)

            with open(module_path, "w+") as module:
                module.write(sample)

            analyze = Analyze(tmpdir)
            summarize(analyze)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().replace("\t", "").replace("\n", "")
        self.assertEqual(output, expected_output)
