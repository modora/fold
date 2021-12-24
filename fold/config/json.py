import json

from fold import ConfigFileParser


class JSONConfigParser(ConfigFileParser):
    @classmethod
    def fromText(cls, text: str) -> dict:
        return json.loads(text)
