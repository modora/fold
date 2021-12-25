import unittest

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
