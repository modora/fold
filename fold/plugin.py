from typing import Any, Optional, TypeVar, List
import importlib

T = TypeVar("T")


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

    def load(self, module: str, name: str, package: Optional[str] = None) -> Plugin:
        """Dynamically load a module and import a plugin

        Args:
            module (str): Name of the module to load
            name (str): Name of the object to
            package (str, optional): Required only if the module name is relative. Defaults to none.

        Returns:
            Plugin: Plugin object loaded

        Raises:
            PluginNotFoundError: The plugin does not exist in the module
            TypeError: Object loaded is not a subclass of the plugin
            ImportError: Failed to load the module
        """
        try:
            obj = self.lazyLoad(module, package)
        except AttributeError as e:
            raise PluginNotFoundError("Plugin does not exist") from e

        if not isinstance(obj, self._plugin):
            raise TypeError("Object is not a plugin")

    def lazyLoad(self, module: str, name: str, package: Optional[str] = None) -> Any:
        """Dynamically load a module and import an object

        A lazier implementation of the load function that doesn't do type checking for the object it imports. This
        method is provided to the user for convenience in the case they want to import an object without creating
        another manager class.

        Args:
            module (str): Name of the module to load
            name (str): Name of the object to load
            package (str, optional): Required only if the module name is relative. Defaults to none.

        Returns:
            Any: Object loaded

        Raises:
            ImportError: Failed to load module
            AttributeError: Object does not exist in module

        """
        m = importlib.import_module(module, package)
        return getattr(m, name)

    def discover(self, module: str) -> List[Plugin]:
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
