# -*- encoding: utf-8 -*-
import tempfile
import unittest

from kojak.cli import argparser


class TestCLI(unittest.TestCase):
    def test_argparser(self):
        parser = argparser()
        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = "{dir}/module.py".format(dir=tmpdir)

            with open(module_path, "w+") as module:
                module.write("test")
            parser.parse_args([])
            parser.parse_args(["."])
            parser.parse_args([module_path])
            parser.parse_args([tmpdir])

            with self.assertRaises(SystemExit):
                parser.parse_args(["/fake"])

            with self.assertRaises(SystemExit):
                parser.parse_args([".", "--unknow", "boum"])
