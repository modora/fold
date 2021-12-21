from typing import Optional, Any
import importlib


def loadObjectDynamically(name: str, package: Optional[str] = None) -> Any:
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
