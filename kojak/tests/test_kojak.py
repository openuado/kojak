# -*- encoding: utf-8 -*-
import ast
import io
import unittest

from kojak.utils import Analyze, Import


sample = '''
import requests
import abc
from foo import bar

def baz():
    pass

class Foo:
    def run(self):
        pass

    def bar(self):
        pass

class Bar:
    pass
'''


class TestKojak(unittest.TestCase):
    def setUp(self):
        self.analyze = Analyze(io.StringIO(sample))
        self.node = self.analyze.root

    def test_parse_file(self):
        self.assertTrue(isinstance(self.node, ast.Module))

    def test_get_imports(self):
        imports = [el for el in self.analyze.get_imports()]
        expected_imports = [
            Import(module=[], name='requests', alias=None),
            Import(module=[], name='abc', alias=None),
            Import(module='foo', name='bar', alias=None)
        ]

        self.assertEqual(imports, expected_imports)

    def test_get_classes(self):
        classes = [el for el in self.analyze.get_classes()]
        self.assertEqual(len(classes), 2)
        self.assertEqual(classes[0].name, 'Foo')
        self.assertEqual(classes[1].name, 'Bar')

        methods = [el for el in self.analyze.get_functions(classes[0].node)]
        self.assertEqual(len(methods), 2)
        self.assertEqual(methods[0].name, 'run')
        self.assertEqual(methods[1].name, 'bar')
