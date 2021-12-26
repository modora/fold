from typing import Optional, Dict, Set
import importlib
from fold.utils import loadObjectDynamically


class Plugin:
    NAME: Optional[str] = None

    @property
    @classmethod
    def name(cls) -> str:
        return cls.NAME or cls.__name__


class PluginManager:
    def __init__(self, obj: Plugin) -> None:
        """Create a plugin manager

        Args:
            obj (Plugin): The plugin class to manage
        """
        self._plugin = obj
        self._cache: Dict[str, Plugin] = {}

    @property
    def cache(self) -> Dict[str, Plugin]:
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
            return self.cache[name]
        try:
            obj = loadObjectDynamically(name, package)
        except AttributeError as e:
            raise ImportError("Plugin does not exist") from e

        if not isinstance(obj, self._plugin):
            raise TypeError("Object is not a plugin")

        if cache:
            self._cache[name] = obj

        return obj

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

        if cache and name in self.cache:
            return self.cache[name]
        m = importlib.import_module(name, package)
        # Check non-private objects whether they are Plugin objects
        plugins: Set[Plugin] = set()
        for obj in [
            getattr(m, name) for name in dir(m) if not name.startswith("_")
        ]:  # get non-private objects
            if issubclass(obj, self._plugin):  # check if plugin
                plugins.add(obj)
        self.cache[name] = plugins
        return plugins
