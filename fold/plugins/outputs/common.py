from __future__ import annotations
from typing import Any, Iterable, Optional, Mapping, TypeVar, Dict
from abc import abstractmethod

from pydantic import BaseModel

from fold.core import Plugin, ConfigManager, Content
from fold.utils.plugin import PluginManager

T_Config = TypeVar("T_Config")


class OutputPluginConfig(BaseModel):
    name: str

    class Config:
        extra = "forbid"


class OutputPlugin(Plugin):
    def __init__(
        self, config: OutputPluginConfig | Iterable[OutputPluginConfig], *args, **kwargs
    ) -> None:
        super().__init__(config, *args, **kwargs)

    @abstractmethod
    def write(self, data: Any):
        """Write data to output

        Args:
            data (Any): Data to publish
        """
        pass


class OutputManager(ConfigManager):
    def __init__(
        self,
        config: OutputPluginConfig | Iterable[OutputPluginConfig],
        plugins: Optional[Mapping[str, OutputPlugin]] = None,
        *args,
        **kwargs
    ) -> None:
        super().__init__(config, *args, **kwargs)
        if plugins is None:
            plugins = self.DEFAULT_PLUGINS

        if isinstance(config, OutputPluginConfig):
            config = [config]

        self.handlers = [plugins[conf.name] for conf in config]

    @classmethod
    @property
    def DEFAULT_PLUGINS(cls) -> Dict[str, OutputPlugin]:
        plugins = PluginManager(OutputPlugin).discover("fold.plugins.outputs")
        return {plugin.__name__: plugin for plugin in plugins}

    @classmethod
    def parseDict(
        cls,
        config: Dict[str, Content],
        plugins: Optional[Mapping[str, OutputPlugin]] = None,
        *args,
        **kwargs
    ) -> OutputPluginConfig:
        if plugins is None:
            plugins = cls.DEFAULT_PLUGINS

        config: OutputPluginConfig = OutputPluginConfig(**config)
        return plugins[config.name].parseConfig(config)

    def write(self, data: Any):
        for handler in self.handlers:
            handler.write(data)
