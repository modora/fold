from fold import PluginManager as _PluginManager

from .common import OutputPlugin
from .stdout import StdoutOutputPlugin

outputPluginManager = _PluginManager(OutputPlugin)
