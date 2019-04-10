# -*- encoding: utf-8 -*-
import io
import sys
import tempfile
import unittest

from kojak.models import Analyze
from kojak.reports import Report

from sample import sample


class TestReport(unittest.TestCase):
    def setUp(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open("{dir}/test.py".format(dir=tmpdir), "w+") as fake:
                fake.write(sample)

            self.tmpdir = tmpdir
            self.analyze = Analyze(tmpdir)

    def test_report(self):
        expected_output = (
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            "Module:{tmpdir}/test.py3imports2classes"
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            "Moduleimports:ImportrequestsImportabcFromfoo"
            "importbarModuleclasses:Bar-run-barFoo"
            "Thisprojecthave:-3imports-2classes".format(tmpdir=self.tmpdir)
        )
        expected_output2 = (
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            "Module:{tmpdir}/test.py3imports2classes"
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            "Moduleimports:ImportrequestsImportabcFromfoo"
            "importbarModuleclasses:FooBar-run-bar"
            "Thisprojecthave:-3imports-2classes".format(tmpdir=self.tmpdir)
        )
        captured_output = io.StringIO()
        sys.stdout = captured_output
        report = Report()
        report.rendering("cli.txt", self.analyze)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        output = output.replace("\t", "").replace("\n", "").replace(" ", "")
        try:
            self.assertEqual(output, expected_output)
        except AssertionError:
            # (hberaud) Python 3.5 list classes in a random order
            # so to avoid assertion errors due to the python 3.5
            # behaviour that is different from python higher versions
            # we want to check the another expected output with
            # classes in different order.
            self.assertEqual(output, expected_output2)
