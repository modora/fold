from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Dict, Set, Any
from abc import ABC, abstractmethod
import importlib

if TYPE_CHECKING:
    from fold.config import Content

from fold.utils import loadObjectDynamically


class Plugin(ABC):
    NAME: Optional[str] = None

    def __init__(self, config: Dict[str, Content], *args, **kwargs) -> None:
        super().__init__()

    @classmethod
    @abstractmethod
    def parseConfig(cls, config: Content) -> Content:
        pass


class Manager(ABC):
    def __init__(self, config: Dict[str, Content], *args, **kwargs) -> None:
        pass

    @classmethod
    @abstractmethod
    def parseConfig(cls, config: Content):
        pass


class PluginManager:
    _cache: Dict[str, Any] = {}

    def __init__(self, obj: Plugin) -> None:
        """Create a plugin manager

        Args:
            obj (Plugin): The plugin class to manage
        """
        self._plugin = obj

    @property
    def cache(self) -> Dict[str, Any]:
        """Importer cache

        Returns:
            Dict[str, Any]: Import cache where the key is the import name and the value is the module/object
        """
        return self._cache

    def flushCache(self):
        """Flush plugin cache"""
        self._cache = {}

    def load(
        self, name: str, package: Optional[str] = None, cache: bool = True
    ) -> Plugin:
        """Dynamically load a module and import a plugin

        Args:
            name (str): Path to object in <module>:<object> notation
            package (str, optional): Required only if the module name is relative. Defaults to None.
            cache (bool, optional): Use cache result. Defaults to True.

        Returns:
            Plugin: Plugin object loaded

        Raises:
            TypeError: Object loaded is not a subclass of the plugin
            ImportError: Failed to load the module
        """

        if cache and name in self.cache:
            obj = self.cache[name]
        else:
            try:
                obj = loadObjectDynamically(name, package)
            except AttributeError as e:
                raise ImportError("Plugin does not exist") from e
            # cache the result
            if cache:
                self._cache[name] = obj

        # return only strict, subclass of Plugin
        if issubclass(obj, self._plugin) and obj is not self._plugin:
            return obj
        raise TypeError("Object is not a plugin")

    def discover(
        self, name: str, package: Optional[str] = None, cache: bool = True
    ) -> Set[Plugin]:
        """Dynamically load a module and return a set of all plugin objects found

        Args:
            name (str): Path to module in dot notation
            package (str, optional): Required only if the module name is relative. Defaults to None.
            cache (bool, optional): Use cache result. Defaults to True.

        Returns:
            Set[Plugin]: Dictionary of plugins discovered in the module in {name: Plugin} format
        """

        # import from the importer cache
        if cache and name in self.cache:
            module = self.cache[name]
        else:  # cache missed or disabled
            module = importlib.import_module(name, package)
            # update cache
            if cache:
                self.cache[name] = module

        # return only non-private plugin objects, ommitting the plugin class itself
        plugins = set()
        for object in [getattr(module, name) for name in dir(module)]:
            try:
                if (
                    issubclass(object, self._plugin)
                    and object is not self._plugin
                    and not object.__name__.startswith("_")
                ):
                    plugins.add(object)
            except TypeError:
                pass
        return plugins
