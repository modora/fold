from __future__ import annotations
from typing import TYPE_CHECKING
import unittest

from fold.plugin import Plugin, PluginManager

if TYPE_CHECKING:
    from fold.config import Content


class TestPluginManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = PluginManager(Plugin)

    def testLoader(self):
        from test.sample_plugin1.p1 import P1

        path = "test.sample_plugin1.p1:P1"
        obj = self.manager.load(path, cache=False)

        self.assertEqual(P1, obj)

    def testLoaderCacheRead(self):
        # Manually override the manager cache. If the cache works, then the loader should return something from the fake
        # path
        class Bar(Plugin):  # Sample plugin
            @classmethod
            def parseConfig(cls, config: Content) -> Content:
                return super().parseConfig(config)

        path = "test.nonexistentpath:foo"
        self.manager._cache = {"test.nonexistentpath:foo": Bar}
        obj = self.manager.load(path, cache=True)
        self.assertEqual(Bar, obj)

    def testLoaderCacheWrite(self):
        from test.sample_plugin1.p1 import P1

        path = "test.sample_plugin1.p1:P1"
        self.manager._cache = {}
        self.manager.load(path, cache=True)

        expected = {path: P1}
        result = self.manager.cache

        self.assertDictEqual(expected, result)

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
