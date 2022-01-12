import unittest
from unittest.mock import patch
from io import StringIO

from pydantic import ValidationError

from fold.outputs.stdout import Stdout, StdoutConfig


class TestStdoutParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parser = Stdout.parseConfig
        cls.MIN_CONFIG = {"name": "test"}

    def _test(self, expected, config):
        # EAFP
        try:
            issubclass(expected, Exception)
        except TypeError:
            result = self.parser(config).dict(exclude_none=True, exclude_unset=True)
            self.assertEqual(expected, result)
        else:
            self.assertRaises(expected, self.parser, config)

    def testMinConfig(self):
        config = self.MIN_CONFIG
        expected = self.MIN_CONFIG
        self._test(expected, config)

    def testExtraKeys(self):
        config = {**self.MIN_CONFIG, **{"foo": "bar"}}
        expected = ValidationError
        self._test(expected, config)

    def testMissingKeys(self):
        """It should raise a KeyError"""
        config = self.MIN_CONFIG.copy()
        key = list(config.keys())[0]  # key to remove
        del config[key]
        expected = ValidationError
        self._test(expected, config)


class TestStdoutWrite(unittest.TestCase):
    def _test(self, expected, data):
        config = StdoutConfig(name="stdout")
        plugin = Stdout(config)
        with patch("sys.stdout", StringIO()) as stdout:
            plugin.write(data)
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
