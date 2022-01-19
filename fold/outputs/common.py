from __future__ import annotations
from typing import TYPE_CHECKING, Any, Mapping, Set, List, Dict, Optional
from abc import abstractmethod

from pydantic import BaseModel

from fold.plugin import Plugin, PluginManager

if TYPE_CHECKING:
    from fold.config import Content


class OutputHandlerConfig(BaseModel):
    name: str

    class Config:
        extra = "allow"


class OutputPlugin(Plugin):
    def __init__(self, config: OutputHandlerConfig, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def write(self, data: Any):
        """Write data to output

        Args:
            data (Any): Data to publish
        """
        pass


class OutputManager(Plugin):
    def __init__(
        self,
        config: List[OutputHandlerConfig],
        plugins: Optional[Mapping[str, OutputPlugin]] = None,
        *args,
        **kwargs
    ) -> None:
        if plugins is None:
            plugins = self.DEFAULT_PLUGINS
        self.handlers: Set[OutputPlugin] = set()

        for conf in config:
            self.handlers.add(plugins[conf.name](config))

    @classmethod
    @property
    def DEFAULT_PLUGINS(cls) -> Dict[str, OutputPlugin]:
        plugins = PluginManager(OutputPlugin).discover("fold.output")
        return {plugin.__name__: plugin for plugin in plugins}

    @classmethod
    def parseConfig(
        cls,
        config,
        plugins: Optional[Mapping[str, OutputPlugin]] = None,
        *args,
        **kwargs
    ):
        if plugins is None:
            plugins = cls.DEFAULT_PLUGINS
        # Validate the base handler keys first, then use the plugin parser to parse the remaining keys. Validation is
        # performed in the pydantic model so we just simply type casting the variable will run the validators
        match config:
            case list():
                config: List[OutputHandlerConfig] = [
                    OutputHandlerConfig(**conf) for conf in config
                ]
                return [plugins[conf.name].parseConfig(**conf) for conf in config]
            case dict():
                config: OutputHandlerConfig = OutputHandlerConfig(**config)
                return plugins[config.name].parseConfig(config)
            case _:
                raise TypeError

    def write(self, data: Any):
        for handler in self.handlers:
            handler.write(data)
