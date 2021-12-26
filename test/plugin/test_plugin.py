import unittest

from fold.plugin import Plugin, PluginManager


class TestPlugin(unittest.TestCase):
    def testNameUndefined(self):
        """Should be name of the class if name not defined"""

        class SamplePlugin(Plugin):
            pass

        expected = "SamplePlugin"
        result = SamplePlugin.name
        self.assertEqual(expected, result)

    def testNameDefined(self):
        class SamplePlugin(Plugin):
            NAME = "fooBar"
            pass

        expected = SamplePlugin.NAME
        result = SamplePlugin.name
        self.assertEqual(expected, result)


class TestPluginManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = PluginManager(Plugin)

    def testFlushCache(self):
        self.manager._cache = {"foo": Plugin}
        expected = {}

        self.manager.flushCache()
        self.assertDictEqual(expected, self.manager.cache)
