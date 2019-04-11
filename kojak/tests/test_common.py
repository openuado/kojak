# -*- encoding: utf-8 -*-
import os
import tempfile
import unittest

from kojak.common import is_valid_path
from kojak.common import python_files


class TestCommon(unittest.TestCase):
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

    def test_python_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = "{dir}/subdir".format(dir=tmpdir)
            os.mkdir(subdir)
            files = [
                "{dir}/README.md".format(dir=tmpdir),
                "{dir}/module.pyc".format(dir=tmpdir),
                "{dir}/module1.py".format(dir=tmpdir),
                "{dir}/module2.py".format(dir=subdir),
            ]

            for el in files:
                with open(el, "w+") as module:
                    module.write("test")
            modules = python_files(tmpdir)
            self.assertEqual(len(modules), 2)
