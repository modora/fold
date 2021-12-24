import json

from .common import ConfigFileParser, Content


class JSONConfigParser(ConfigFileParser):
    EXTENSIONS = {"json"}

    @classmethod
    def fromText(cls, text: str) -> Content:
        return json.loads(text)
