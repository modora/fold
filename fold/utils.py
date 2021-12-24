from typing import Optional, Any, Tuple, List
import re
import importlib


def parseModuleObjectString(string: str) -> Tuple[str, str]:
    """Parse a string using the notation <module>.<object>

    Args:
        string (str): String to parse

    Raises:
        ValueError: Unable to parse string

    Returns:
        Tuple[str, str]: (module, object)

    """

    # We split the name at each "." and the final element is the object name, everything prior is the module name.
    # I am choosing to implement using regex over str.split because I don't know how Python will handle non-ASCII
    # modules and objects. Regex will enforce ASCII only

    matches: List[str]
    # Module
    if not (matches := re.findall(r"(\w+)\.", string)):
        raise ValueError(f"Unable to parse module in {string}")
    module = ".".join(matches)

    # Object
    if not (matches := re.findall(r"\.(\w+)", string)):
        raise ValueError(f"Unable to parse object in {string}")
    obj = matches[-1]

    return (module, obj)


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

    moduleName, objectName = parseModuleObjectString(name)

    m = importlib.import_module(moduleName, package)
    return getattr(m, objectName)
