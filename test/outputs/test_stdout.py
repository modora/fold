import unittest
from unittest.mock import patch
from io import StringIO

from fold.output.stdout import StdoutOutputPlugin


class TestStdoutParser(unittest.TestCase):
    def _test(self, expected, config):
        result = StdoutOutputPlugin.parseConfig(config)
        self.assertEqual(expected, result)

    def testNullConfig(self):
        config = None
        expected = None
        self._test(expected, config)

    def testEmptyDictConfig(self):
        config = {}
        expected = None
        self._test(expected, config)

    def testNonEmptyConfig(self):
        """It should ignore the config and return None"""
        config = {"foo": "bar", "hello": 123}
        expected = None
        self._test(expected, config)


class TestStdoutWrite(unittest.TestCase):
    def _test(self, expected, data):
        with patch("sys.stdout", StringIO()) as stdout:
            StdoutOutputPlugin(None).write(data)
            result = stdout.getvalue()
            self.assertEqual(expected, result)

    def testEmptyString(self):
        data = ""
        expected = "\n"
        self._test(expected, data)

    def testFoo(self):
        data = "foo"
        expected = "foo\n"
        self._test(expected, data)

    def testNull(self):
        """Should be equivalent to empty line"""
        data = None
        expected = "\n"
        self._test(expected, data)
