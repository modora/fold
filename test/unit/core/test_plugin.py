import unittest

from fold.core.plugin import Plugin

from fold.utils.plugin import PluginManager


class TestPlugin(unittest.TestCase):
    def testNoSubclass(self):
        """If user does not subclass the Plugin class, then raise TypeError"""
        self.assertRaises(TypeError, Plugin)


class TestPluginManagerCacheFlush(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = PluginManager(Plugin)

    def testFlushCache(self):
        initialCache = {"foo": Plugin}
        self.manager._cache = initialCache
        self.assertDictEqual(
            initialCache,
            self.manager.cache,
            "Test is invalid, cache not initialized correctly",
        )

        expected = {}
        self.manager.flushCache()
        self.assertDictEqual(expected, self.manager.cache)


class TestPluginManagerLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = PluginManager(Plugin)

    def setUp(self) -> None:
        self.manager._cache = {}

    def testLoader(self):
        from .sample_plugins.p1 import P1

        path = "tests.unit.core.sample_plugins.p1:P1"
        obj = self.manager.load(path, cache=False)

        self.assertEqual(P1, obj)

    def testCacheRead(self):
        class Bar(Plugin):  # Sample plugin
            @classmethod
            def parseConfig(cls, config):
                return super().parseConfig(config)

        path = "tests.nonexistentpath:foo"
        self.manager._cache = {path: Bar}
        obj = self.manager.load(path, cache=True)
        self.assertEqual(Bar, obj)

    def testCacheWrite(self):
        from .sample_plugins.p1 import P1

        path = "tests.unit.core.sample_plugins.p1:P1"
        self.manager.load(path, cache=True)

        expected = {path: P1}
        result = self.manager.cache

        self.assertDictEqual(expected, result)


class TestPluginManagerDiscovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = PluginManager(Plugin)

    def setUp(self) -> None:
        self.manager._cache = {}

    def testDiscoverMethod(self):
        from .sample_plugins import P1, P2

        expected = {P1, P2}
        path = "tests.unit.core.sample_plugins"
        plugins = self.manager.discover(path, cache=False)
        self.assertSetEqual(expected, plugins)

    def testCacheRead(self):
        class FakeModule:
            class NotAPlugin:
                pass

            class FakePlugin(Plugin):
                @classmethod
                def parseConfig(cls, config):
                    return config

        path = "fake.path"
        self.manager._cache = {path: FakeModule}
        plugins = self.manager.discover(path, cache=True)
        expected = {FakeModule.FakePlugin}

        self.assertSetEqual(expected, plugins)

    def testCacheWrite(self):
        import test.unit.core.sample_plugins

        path = "tests.unit.core.sample_plugins"
        self.manager.discover(path, cache=True)
        expected = {path: test.unit.sample_plugins}
        self.assertDictEqual(expected, self.manager.cache)
