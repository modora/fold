import unittest
from unittest.mock import patch
from io import StringIO

from fold.outputs.stdout import Stdout, StdoutConfig


class TestStdoutParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parser = Stdout.parseConfig

    def _test(self, expected, config):
        # EAFP
        try:
            issubclass(expected, Exception)
        except TypeError:
            result = self.parser(config)
            self.assertEqual(expected, result)
        else:
            self.assertRaises(expected, self.parser, config)

    def testMinConfig(self):
        config = StdoutConfig(name="test")
        expected = {"name": "test"}
        self._test(expected, config)

    def testExtraKeys(self):
        """It should preserve the keys"""
        config = StdoutConfig(name="test")
        config = {**config, **{"foo": "bar"}}
        expected = {"name": "test", "foo": "bar"}
        self._test(expected, config)

    def testMissingKeys(self):
        """It should raise a KeyError"""
        config = {}
        expected = KeyError
        self._test(expected, config)


class TestStdoutWrite(unittest.TestCase):
    def _test(self, expected, data):
        with patch("sys.stdout", StringIO()) as stdout:
            Stdout().write(data)
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
