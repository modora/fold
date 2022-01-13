from typing import Optional, Any
import importlib
from .modObjStr import parseModuleObjectString, parseObjectAttrString


def importFromString(name: str, package: Optional[str] = None) -> Any:
    """Dynamically load a module or object in <module>:<object> notation

    Args:
        name (str): Path to object in <module>:<object> notation
        package (str, optional): Required only if the module name is relative. Defaults to none.

    Returns:
        Any: Object loaded

    Raises:
        ImportError: Failed to load module
        AttributeError: Object does not exist in module

    """

    moduleName, objectString = parseModuleObjectString(name)

    m = importlib.import_module(moduleName, package)

    if objectString is None:
        return m
    objectName, attrs = parseObjectAttrString(objectString)
    obj = getattr(m, objectName)
    for attr in attrs:
        obj = getattr(m, attr)
    return obj
