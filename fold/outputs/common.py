from typing import Any
from fold import Plugin
import abc


class OutputPlugin(Plugin):
    @abc.abstractmethod
    def __init__(self, config) -> None:
        pass

    @abc.abstractmethod
    def write(self, data: Any):
        pass
