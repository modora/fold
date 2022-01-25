from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from pydantic import BaseModel

if TYPE_CHECKING:
    from .config import Content


class Plugin(ABC):
    def __init__(self, config: BaseModel, *args, **kwargs) -> None:
        self.config = config

    @classmethod
    @abstractmethod
    def parseConfig(cls, config: Content, *args, **kwargs) -> BaseModel:
        pass
