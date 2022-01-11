import unittest
import sys
from pathlib import Path

from pydantic import ValidationError

from fold.logger.logger import LogHandlerConfig


class TestLogConfig(unittest.TestCase):
    def _test(self, expected: dict, content: dict):
        actual = LogHandlerConfig(**content).dict()

        # remove the optional keys
        actual = {k: v for k, v in actual.items() if v is not None}

        self.assertDictEqual(actual, expected)

    def _testRaises(self, expected: Exception, content: dict):
        self.assertRaises(expected, LogHandlerConfig, **content)

    def testFooSink(self):
        content = {"sink": "foo"}
        expected = {"sink": Path("foo")}

        self._test(expected, content)

    def testBarPathSink(self):
        content = {"sink": Path("bar")}
        expected = {"sink": Path("bar")}

        self._test(expected, content)

    def testStdoutSink(self):
        content = {"sink": "custom", "custom_sink": "sys:stdout"}
        expected = {"sink": sys.stdout}

        self._test(expected, content)

    def testStderrSink(self):
        content = {"sink": "stderr"}
        expected = {"sink": sys.stderr}

        self._test(expected, content)

    def testUnknownKeyError(self):
        content = {"foo": False}

        self._testRaises(ValidationError, content)
