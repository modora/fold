import toml

from fold import ConfigFileParser


class TOMLConfigParser(ConfigFileParser):
    @classmethod
    def fromText(cls, text: str) -> dict:
        return toml.loads(text)
