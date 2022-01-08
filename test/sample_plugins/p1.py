from __future__ import annotations
from typing import TYPE_CHECKING
from fold.plugin import Plugin

if TYPE_CHECKING:
    from fold.config import Content


class P1(Plugin):
    @classmethod
    def parseConfig(cls, config: Content) -> Content:
        return config
