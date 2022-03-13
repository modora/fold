from unittest import TestCase
from pydantic import ValidationError
from fold.plugins.outputs.common import OutputPlugin, OutputManager, OutputPluginConfig


class TestOutputHandlerConfig(TestCase):
    def _test(self, expected: dict | Exception, config: dict):
        cls = OutputPluginConfig
        try:
            issubclass(expected, Exception)
        except TypeError:
            actual = cls(**config)
            self.assertDictEqual(
                expected, actual.dict(exclude_none=True, exclude_unset=True)
            )
        else:
            self.assertRaises(expected, cls, **config)

    @classmethod
    def setUpClass(cls) -> None:
        cls.minConfig = {"name": "handlerName"}

    def testMinConfig(self):
        self._test(self.minConfig, self.minConfig)

    def testExtraKeys(self):
        """Should raise a ValidationError"""
        config = {**self.minConfig, **{"foo": "bar"}}
        expected = ValidationError
        self._test(expected, config)


class TestOutputPlugin(TestCase):
    def testInstance(self):
        """Plugin should be ABC so creating an instance should fail"""
        self.assertRaises(TypeError, OutputPlugin)


class TestOutputManager(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.minConfig = OutputPluginConfig(name="foo")

        class MockPlugin:
            def __init__(self, config, *args, **kwargs) -> None:
                self.inputs = (config, args, kwargs)

        cls.mockPlugins = {"foo": MockPlugin}

    def testDefaultPlugins(self):
        import fold.plugins.outputs as outputs

        plugins = {}
        for name in dir(outputs):
            obj = getattr(outputs, name)
            try:
                result = issubclass(obj, OutputPlugin) and obj is not OutputPlugin
            except TypeError:
                pass
            else:
                if result:
                    plugins[obj.__name__] = obj

        self.assertDictEqual(plugins, OutputManager.DEFAULT_PLUGINS)

    def testInit(self):
        with self.subTest("Min config"):
            manager = OutputManager(self.minConfig, plugins=self.mockPlugins)
            with self.subTest("handlers"):
                self.assertSetEqual(manager.handlers, set())
            with self.subTest("plugins"):
                self.assertDictEqual(manager.plugins, self.mockPlugins)
