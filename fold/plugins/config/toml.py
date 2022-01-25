from typing import Dict

import toml

from fold.core import Content
from .common import ConfigFilePlugin


class TOMLConfig(ConfigFilePlugin):
    EXTENSIONS = {"toml"}

    @classmethod
    def fromText(cls, text: str) -> Dict[str, Content]:
        return toml.loads(text)
