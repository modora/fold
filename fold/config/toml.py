from typing import Dict

import toml

from .common import ConfigFilePlugin, Content


class TOMLConfig(ConfigFilePlugin):
    EXTENSIONS = {"toml"}

    @classmethod
    def fromText(cls, text: str) -> Dict[str, Content]:
        return toml.loads(text)
