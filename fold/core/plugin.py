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

    def load(self, name: str, package: Optional[str] = None) -> Plugin:
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
            obj = self.lazyLoad(module, package)
        except AttributeError as e:
            raise PluginNotFoundError("Plugin does not exist") from e

        if not isinstance(obj, self._plugin):
            raise TypeError("Object is not a plugin")

    def lazyLoad(self, name: str, package: Optional[str] = None) -> Any:
        """Dynamically load a module and import an object

        A lazier implementation of the load function that doesn't do type checking for the object it imports. This
        method is provided to the user for convenience in the case they want to import an object without creating
        another manager class.

        Args:
            name (str): Path to object in <module>.<object> notation
            package (str, optional): Required only if the module name is relative. Defaults to none.

        Returns:
            Any: Object loaded

        Raises:
            ImportError: Failed to load module
            AttributeError: Object does not exist in module

        """

        # We split the name at each "." and the final element is the object name, everything prior is the module name.
        l = name.split(".")
        moduleName = "".join(l[:-2])
        objectName = l[-1]

        m = importlib.import_module(moduleName, package)
        return getattr(m, objectName)

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
