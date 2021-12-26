from typing import Tuple, Optional, Any, List
import re
import importlib


def parseModuleObjectString(string: str) -> Tuple[str, str]:
    """Parse a string using the notation <module>:<object>

    Args:
        string (str): String to parse

    Raises:
        ValueError: Unable to parse string

    Returns:
        Tuple[str, str]: (module, object)

    """

    # I am choosing to implement using regex over str.split because regex handles character checks

    pattern = r"([\w\.]+):?([\w\.]+)?"
    if not (match := re.match(pattern, string)):
        raise ValueError(f"Unable to parse string {string}")

    return (match.group(1), match.group(2))


def parseObjectString(string: str) -> Tuple[str, List[str]]:
    pattern = re.compile(r"(\w+)")
    matches = pattern.findall(string)

    return (matches[0], matches[1:])


def loadObjectDynamically(name: str, package: Optional[str] = None) -> Any:
    """Dynamically load a module or object

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
    objectName, attrs = parseObjectString(objectString)
    obj = getattr(m, objectName)
    for attr in attrs:
        obj = getattr(m, attr)
    return obj
