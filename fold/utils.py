from typing import Tuple
import re


def parseModuleObjectString(string: str) -> Tuple[str, str]:
    """Parse a string using the notation <module>/<object>

    Args:
        string (str): String to parse

    Raises:
        ValueError: Unable to parse string

    Returns:
        Tuple[str, str]: (module, object)

    """

    # We split the name at each "." and the final element is the object name, everything prior is the module name.
    # I am choosing to implement using regex over str.split because regex handles character checks

    pattern = r"([\w\.]+)\/(\w+)"
    if not (match := re.match(pattern, string)):
        raise ValueError(f"Unable to parse string {string}")

    return (match.group(0), match.group(1))
