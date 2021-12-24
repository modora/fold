import toml

from .common import ConfigFileParser, Content


class TOMLConfigParser(ConfigFileParser):
    EXTENSIONS = {"toml"}

    @classmethod
    def fromText(cls, text: str) -> Content:
        return toml.loads(text)
