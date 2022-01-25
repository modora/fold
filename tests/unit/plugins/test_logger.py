import unittest
import sys
from pathlib import Path

from pydantic import ValidationError

from fold.plugins.logger.logger import LogHandlerConfig


class TestLogConfig(unittest.TestCase):
    def _test(self, expected: dict, content: dict):
        actual = LogHandlerConfig(**content).dict(exclude_none=True, exclude_unset=True)

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
