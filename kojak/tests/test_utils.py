# -*- encoding: utf-8 -*-
import ast
import io
import tempfile
import unittest

from kojak.exceptions import KojakException
from kojak.utils import Analyze
from kojak.utils import Import
from kojak.utils import Module

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
        imports = [el for el in self.module.get_imports()]
        self.assertEqual(len(imports), 3)
        expected_imports = [
            Import(module=[], name='requests', alias=None),
            Import(module=[], name='abc', alias=None),
            Import(module='foo', name='bar', alias=None)
        ]

        self.assertEqual(imports, expected_imports)

    def test_get_classes(self):
        classes = [el for el in self.module.get_classes()]
        self.assertEqual(len(classes), 2)
        self.assertEqual(classes[0].name, 'Bar')
        self.assertEqual(classes[1].name, 'Foo')

        methods = [el for el in self.module.get_functions(classes[0].node)]
        self.assertEqual(len(methods), 2)
        self.assertEqual(methods[0].name, 'run')
        self.assertEqual(methods[1].name, 'bar')


class TestAnalyze(unittest.TestCase):
    def setUp(self):
        self.pyfile = io.StringIO(sample)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)
        self.node = self.module.root
        self.imports_number = len([el for el in self.module.get_imports()])
        self.classes_number = len([el for el in self.module.get_classes()])
        fake_files = ["one", "two", "three"]
        with tempfile.TemporaryDirectory() as tmpdir:
            for el in fake_files:
                fake = open("{dir}/{name}.py".format(
                    dir=tmpdir, name=el), "w+")
                fake.write(sample)
            fake = open("{dir}/test.txt".format(dir=tmpdir), "w+")

            self.tmpdir = tmpdir
            self.analyze = Analyze(tmpdir)
            self.modules = [el for el in self.analyze.get_modules()]

    def test_modules(self):
        self.assertEqual(len(self.modules), 3)

    def test_global_stats(self):
        self.stats = self.analyze.get_global_stats()
        self.assertEqual(
            self.stats['imports'],
            self.imports_number * len(self.modules))
        self.assertEqual(
            self.stats['classes'],
            self.classes_number * len(self.modules))

    def test_analyze_on_single_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = "{dir}/module.py".format(dir=tmpdir)
            with open(module_path, "w+") as module:
                module.write(sample)

            sh_path = "{dir}/script.sh".format(dir=tmpdir)
            with open(sh_path, "w+") as sh:
                sh.write('echo test!')

            self.analyze = Analyze(module_path)

            with self.assertRaises(KojakException):
                self.analyze = Analyze(sh_path)

            try:
                fake = "{dir}/fake".format(dir=tmpdir)
                self.analyze = Analyze(fake)
            except KojakException as err:
                self.assertEqual(str(err), 'Path not found: {fake}'.format(
                    fake=fake))
