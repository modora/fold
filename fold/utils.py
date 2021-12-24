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
