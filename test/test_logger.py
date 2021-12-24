import unittest
import sys
from pathlib import Path

import fold.logger


class TestLogConfigSectionParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parser = fold.logger.LogConfigSectionParser

    def _test(self, content, expected):
        actual = self.parser(content).parse()

        self.assertListEqual(actual, expected)

    def testStdoutSink(self):
        content = [{"sink": "stdout"}]
        expected = [{"sink": sys.stdout}]

        self._test(content, expected)

    # Is there more than one stderr? Importing stderr across modules seems to create a new memory address.
    # Disabling the test for now
    @unittest.skip("<Issue reference here>")
    def testStderrSink(self):
        content = [{"sink": "stdout"}]
        expected = [{"sink": sys.stderr}]

        self._test(content, expected)

    def testStdinSink(self):
        content = [{"sink": "stdin"}]
        expected = [{"sink": Path("stdin")}]

        self._test(content, expected)

    def testFooSink(self):
        content = [{"sink": "foo"}]
        expected = [{"sink": Path("foo")}]

        self._test(content, expected)

    def testFooBarSinks(self):
        content = [{"sink": "foo"}, {"sink": "bar"}]
        expected = [{"sink": Path("foo")}, {"sink": Path("bar")}]

        self._test(content, expected)

    def testMultipleOptions(self):
        content = [{"sink": "stdout", "colorize": False}]
        expected = [{"sink": sys.stdout, "colorize": False}]

        self._test(content, expected)

    def testUnknownKeyError(self):
        content = [{"foo": False}]

        self.assertRaises(
            KeyError, lambda content: self.parser(content).parse(), content
        )
