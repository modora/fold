from typing import Any, Iterable, Set, TypedDict, Optional, List, Dict
import abc
from build.lib.fold.core.plugin import PluginManager

from fold.core import Plugin
from fold.config import Content
from fold.core.plugin import Manager
from fold.utils import parseModuleObjectString


class OutputHandlerConfig(TypedDict):
    name: str


OutputConfig = List[OutputHandlerConfig]


class OutputPlugin(Plugin):
    def __init__(self, config: Dict[str, Content], *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def write(self, data: Any):
        """Write data to output

        Args:
            data (Any): Data to publish
        """
        pass


class OutputManager(Manager):
    NAME = "output"

    def __init__(self, config: Dict[str, Content], *args, **kwargs) -> None:
        outputConfig = config["output"]
        self.handlers: Set[OutputPlugin] = set()
        plugins = self.DEFAULT_PLUGINS

        handlerConfig: OutputHandlerConfig
        for handlerConfig in outputConfig:
            name = handlerConfig["name"]
            handler = plugins[name]
            self._handlers.add(handler(config))

    @classmethod
    @property
    def DEFAULT_PLUGINS(cls) -> Dict[str, OutputPlugin]:
        plugins = PluginManager(OutputPlugin).discover("fold.output")
        return {plugin.name: plugin for plugin in plugins}

    @classmethod
    def parseConfig(cls, config: OutputConfig) -> OutputConfig:
        parsedConfigs = []
        plugins = cls.DEFAULT_PLUGINS
        for conf in config:
            name = conf["name"]
            outputHandler = plugins[name]
            parsedConfigs.append(outputHandler.parseConfig(conf))
        return parsedConfigs

    def write(self, data: Any):
        for handler in self.handlers:
            handler.write(data)
