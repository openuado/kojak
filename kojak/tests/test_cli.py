# -*- encoding: utf-8 -*-
import io
import os
import tempfile
import unittest

from kojak.common import is_valid_path
from kojak.models import Module

from sample import sample


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.pyfile = io.StringIO(sample)
        self.pyfile.name = "/fake/module"
        self.module = Module(self.pyfile)

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
