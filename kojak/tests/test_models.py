# -*- encoding: utf-8 -*-
import ast
import io
import tempfile
import unittest

from kojak.exceptions import KojakException
from kojak.models import Analyze
from kojak.models import Import
from kojak.models import Module

from sample import sample


class TestModules(unittest.TestCase):
    def setUp(self):
        self.pyfile = io.StringIO(sample)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)
        self.node = self.module.root

    def test_parse_file(self):
        self.assertTrue(isinstance(self.node, ast.Module))

    def test_name(self):
        self.assertTrue(self.module.name, self.pyfile.name)

    def test_get_imports(self):
        imports = self.module.imports
        self.assertEqual(len(imports), 3)
        expected_imports = [
            Import(module=[], name="requests", alias=None),
            Import(module=[], name="abc", alias=None),
            Import(module="foo", name="bar", alias=None),
        ]

        self.assertEqual(imports, expected_imports)

    def test_get_classes(self):
        classes = self.module.classes
        self.assertEqual(len(classes), 2)
        self.assertEqual(classes[0].name, "Bar")
        self.assertEqual(classes[1].name, "Foo")

        methods = self.module.classes[0].methods
        self.assertEqual(len(methods), 2)
        self.assertEqual(methods[0].name, "run")
        self.assertEqual(methods[1].name, "bar")


class TestAnalyze(unittest.TestCase):
    def setUp(self):
        self.fake_files = ["one", "two", "three"]
        self.get_stats_for_single_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            for el in self.fake_files:
                fake = open(
                    "{dir}/{name}.py".format(dir=tmpdir, name=el), "w+"
                )
                fake.write(sample)
            fake = open("{dir}/test.txt".format(dir=tmpdir), "w+")

            self.tmpdir = tmpdir
            self.analyze = Analyze(tmpdir)
            print(self.analyze.modules)

    def get_stats_for_single_module(self):
        self.pyfile = io.StringIO(sample)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)
        self.node = self.module.root
        self.imports_number = len(self.module.imports)
        self.classes_number = len(self.module.classes)

    def get_expected_modules_len(self):
        return len(self.fake_files)

    def get_expected_total_imports(self):
        return self.get_expected_modules_len() * self.imports_number

    def get_expected_total_classes(self):
        return self.get_expected_modules_len() * self.classes_number

    def test_modules(self):
        self.assertEqual(
            len(self.analyze.modules),
            self.get_expected_modules_len())

    def test_module_imports(self):
        self.assertEqual(
            len(self.analyze.modules[0].imports), self.imports_number)

    def test_module_classes(self):
        self.assertEqual(
            len(self.analyze.modules[0].classes), self.classes_number)

    def test_modules_total_imports(self):
        self.assertEqual(
            self.analyze.imports, self.get_expected_total_imports())

    def test_modules_total_classes(self):
        self.assertEqual(
            self.analyze.classes, self.get_expected_total_classes())

    def test_analyze_on_single_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = "{dir}/module.py".format(dir=tmpdir)
            with open(module_path, "w+") as module:
                module.write(sample)

            sh_path = "{dir}/script.sh".format(dir=tmpdir)
            with open(sh_path, "w+") as sh:
                sh.write("echo test!")

            self.analyze = Analyze(module_path)

            with self.assertRaises(KojakException):
                self.analyze = Analyze(sh_path)

            try:
                fake = "{dir}/fake".format(dir=tmpdir)
                self.analyze = Analyze(fake)
            except KojakException as err:
                self.assertEqual(
                    str(err), "Path not found: {fake}".format(fake=fake)
                )
