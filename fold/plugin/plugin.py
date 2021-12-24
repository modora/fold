from typing import Optional, List, Dict
import importlib
from fold.utils import parseModuleObjectString


class Plugin:
    NAME: Optional[str] = None

    @property
    def name(self) -> str:
        return self.NAME or self.__class__.__name__


class PluginManager:
    def __init__(self, obj: Plugin) -> None:
        """Create a plugin manager

        Args:
            obj (Plugin): The plugin class to manage
        """
        self._plugin = obj
        self._cache: Dict[str, Plugin] = {}

    @property
    def cache(self) -> Plugin:
        return self._cache

    @cache.setter
    def cache(self, value: Plugin):
        # use Plugin.NAME attribute if defined; otherwise, default to the class name
        name = getattr(value, "NAME") or value.__name__
        self._cache[name] = value

    def load(
        self, name: str, package: Optional[str] = None, cache: Optional[bool] = True
    ) -> Plugin:
        """Dynamically load a module and import a plugin

        Args:
            name (str): Path to object in <module>.<object> notation
            package (str, optional): Required only if the module name is relative. Defaults to none.
            cache (bool, optional): Use cache result

        Returns:
            Plugin: Plugin object loaded

        Raises:
            TypeError: Object loaded is not a subclass of the plugin
            ImportError: Failed to load the module
        """

        if cache and name in self._cache:
            return self._cache[name]
        try:
            moduleName, objectName = parseModuleObjectString(name)

            module = importlib.import_module(moduleName, package)
            obj = getattr(module, objectName)
        except AttributeError as e:
            raise ImportError("Plugin does not exist") from e

        if not isinstance(obj, self._plugin):
            raise TypeError("Object is not a plugin")

        self._cache = obj

        return obj

    def discover(self, module: str, cache: Optional[bool] = True) -> List[Plugin]:
        """Dynamically load a module and return a list of all plugin objects found

        Args:
            module (str): Name of the module to load
            cache (bool, optional): Use cache result

        Returns:
            List[Plugin]: List of plugins discovered in the module
        """

        m = importlib.import_module(module)
        # Check non-private objects whether they are Plugin objects
        plugins: List[Plugin] = []
        for obj in [
            getattr(m, name) for name in dir(m) if not name.startswith("_")
        ]:  # get non-private objects
            if issubclass(obj, self._plugin):  # check if plugin
                obj: Plugin
                self._cache = obj
                plugins.append(obj)
        return plugins