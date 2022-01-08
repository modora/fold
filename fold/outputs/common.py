from typing import TYPE_CHECKING, Any, Set, TypedDict, List, Dict
from abc import abstractmethod

from fold.core import Plugin, PluginManager, Manager

if TYPE_CHECKING:
    from fold.config import Config


class OutputHandlerConfig(TypedDict):
    name: str


OutputConfig = List[OutputHandlerConfig]


class OutputPlugin(Plugin):
    def __init__(self, config: Config, *args, **kwargs) -> None:
        pass

    @classmethod
    @property
    def name(cls) -> str:
        return cls.__name__

    @abstractmethod
    def write(self, data: Any):
        """Write data to output

        Args:
            data (Any): Data to publish
        """
        pass


class OutputManager(Manager):
    def __init__(self, config: Config, *args, **kwargs) -> None:
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
