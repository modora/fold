import re
from typing import Tuple, List


def parseModuleObjectString(string: str) -> Tuple[str, str]:
    """Parse a string using the notation <module>:<object>

    Args:
        string (str): String to parse

    Raises:
        ValueError: Unable to parse string

    Returns:
        Tuple[str, str]: (module, object)

    Examples:
        pathlib:Path        <=> (pathlib, Path)
        os.path:abspath     <=> (os.path, abspath)
        .math:sqrt          <=> (.math, abspath)
        abc:ABC.__name__    <=> (abc, ABC.__name__)


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


def parseObjectAttrString(string: str) -> Tuple[str, List[str]]:
    """Parse an object-attribute string in the form <object>.<attr>

    Args:
        string (str): String in the form <object>.<attr>

    Returns:
        Tuple[str, List[str]]: (objectName, List[attrName])
    """
    pattern = re.compile(r"\w+")
    matches = pattern.findall(string)

    return (matches[0], matches[1:])
