from typing import Any
import abc

from fold import Plugin


class OutputPlugin(abc.ABC, Plugin):
    @abc.abstractmethod
    def __init__(self, config) -> None:
        pass

    @abc.abstractmethod
    def write(self, data: Any):
        pass
