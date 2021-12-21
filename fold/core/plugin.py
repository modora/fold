from typing import Optional as _Optional, List as _List
import importlib
from .common import loadObjectDynamically as _loadObjectDynamically


class Plugin:
    pass


class PluginNotFoundError(AttributeError):
    pass


class PluginManager:
    def __init__(self, obj: Plugin) -> None:
        """Create a plugin manager

        Args:
            obj (Plugin): The plugin class to manage
        """
        self._plugin = obj

    def load(self, name: str, package: _Optional[str] = None) -> Plugin:
        """Dynamically load a module and import a plugin

        Args:
            name (str): Path to object in <module>.<object> notation
            package (str, optional): Required only if the module name is relative. Defaults to none.

        Returns:
            Plugin: Plugin object loaded

        Raises:
            PluginNotFoundError: The plugin does not exist in the module
            TypeError: Object loaded is not a subclass of the plugin
            ImportError: Failed to load the module
        """
        try:
            obj = _loadObjectDynamically(name, package)
        except AttributeError as e:
            raise PluginNotFoundError("Plugin does not exist") from e

        if not isinstance(obj, self._plugin):
            raise TypeError("Object is not a plugin")

    def discover(self, module: str) -> _List[Plugin]:
        """Dynamically load a module and return a list of all plugin objects found

        Args:
            module (str): Name of the module to load

        Returns:
            List[Plugin]: List of plugins discovered in the module
        """

        m = importlib.import_module(module)
        # Return a list of non-private, plugin objects
        return [
            obj
            for obj in dir(m)
            if not obj.__name__.startswith("_") and issubclass(obj, self._plugin)
        ]
