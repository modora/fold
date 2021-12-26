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

    # Use regex for character enforcement/filtering
    # This regex pattern seperates the captures the module and object name. The names must be alpha-numeric, "_", or "."
    # The object name is optional
    pattern = r"([\w\.]+):?([\w\.]+)?"
    if not (match := re.match(pattern, string)):
        raise ValueError(f"Unable to parse string {string}")

    moduleName, objectName = match.group(1, 2)

    # Names can still be invalid such as "module.:object" and "module..submodule". This step corrects these issues
    # We can use the re.findall to preserve only the words and add properly formatted dots afterwards.
    # Preserve the leading dots
    if match := re.match(r"^\.+", moduleName):
        leadingDots = match.group(0)
    else:
        leadingDots = ""
    matches = re.findall(r"\w+", moduleName)
    moduleName = leadingDots + ".".join(matches)

    # If object exists, fix invlaid names
    if objectName:
        matches = re.findall(r"\w+", objectName)
        objectName = ".".join(matches)

    return (moduleName, objectName)


def parseObjectString(string: str) -> Tuple[str, List[str]]:
    pattern = re.compile(r"\w+")
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
