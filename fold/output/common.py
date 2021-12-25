from typing import Any, Iterable, TypedDict, Optional, List, Dict
import abc

from fold.plugin import Plugin, PluginManager
from fold.config import ConfigSectionParser, Content
from fold.utils import parseModuleObjectString


class OutputSection(TypedDict):
    type: str
    args: Optional[Content]


class OutputPlugin(abc.ABC, Plugin):
    NAME: str = None

    @abc.abstractmethod
    def __init__(self, config: List[OutputSection]) -> None:
        pass

    @classmethod
    @abc.abstractmethod
    def parseConfig(cls, config: Optional[Content]) -> Optional[Content]:
        """Parse the output args config

        Args:
            config (Content): Arguments dict
        Returns:
            Optional[Content]: Parsed config
        """
        pass

    @abc.abstractmethod
    def write(self, data: Any):
        pass


class OutputSectionParser(ConfigSectionParser):
    def __init__(self, content: List[OutputSection]) -> None:
        super().__init__(content)
        self.content: List[OutputSection]

    def parse(
        self,
        paths: Optional[Iterable[str]] = None,
        *args,
        **kwargs,
    ) -> List[OutputSection]:
        """Parse the output config section

        Args:
            paths (Iterable[str], optional): Iterable string of modules in dot notation or objects to search for plugins. Defaults to {fold.outputs}.
        Returns:
            List[ParsedOutputSection]: Parsed output
        Raises:
            TypeError: Invalid configuration
            KeyError: Output plugin not found
        """
        if not paths:
            paths = ["fold.output"]
        pluginClass = kwargs.get("pluginClass", OutputPlugin)

        parsedSection: List[OutputSection] = []
        manager = PluginManager(pluginClass)

        for rawOutput in self.content:
            if not isinstance(rawOutput, OutputSection):
                raise TypeError(f"Invalid configuration: {rawOutput}")

            parsedOutput: OutputSection = {}
            parsedOutput["type"] = rawOutput["type"]
            parsedOutput["args"] = self._parseArgsConfig(rawOutput, paths, manager)

            # double-chuck the parsedOutput is valid
            if not isinstance(parsedOutput, OutputSection):
                raise RuntimeError("Failed correctly parse output config")

            parsedSection.append(parsedOutput)
        return parsedSection

    @classmethod
    def _loadPlugins(
        cls, paths: Iterable[str], manager: PluginManager
    ) -> Dict[str, OutputPlugin]:
        plugins: Dict[str, OutputPlugin] = {}
        for path in paths:
            # Try to parse the module-string. If it works, then it's a module; otherwise, it's an object.
            try:
                parseModuleObjectString(path)
            except ValueError:  # it's a module
                plugins.update(
                    {plugin.name: plugin for plugin in manager.discover(path)}
                )
            else:
                plugin = manager.load(path)
                plugins.update({plugin.name: plugin})
        return plugins

    @classmethod
    def _parseArgsConfig(
        cls, content: OutputSection, paths: Iterable[str], manager: PluginManager
    ) -> Optional[Content]:
        plugins = cls._loadPlugins(
            paths, manager
        )  # collect all the known output formats
        type = content["type"]
        if not (args := content.get("args")):
            return
        try:
            plugin = plugins[type]
        except KeyError as e:
            raise KeyError(
                f"Unable to find suitable plugin to handle output type {type}"
            ) from e

        return plugin.parseConfig(args)
