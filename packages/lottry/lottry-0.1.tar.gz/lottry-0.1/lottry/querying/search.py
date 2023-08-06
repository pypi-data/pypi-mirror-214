import urllib.parse
from typing import Optional

from pydantic import BaseModel


class Search(BaseModel):
    key: str
    condition: Optional[str]

    def expression(self) -> str:
        ...


class Equals(Search):
    condition: str

    def expression(self) -> str:
        return urllib.parse.quote_plus(f"{self.key}={self.condition}")


class NotEquals(Search):
    condition: str

    def expression(self) -> str:
        return urllib.parse.quote_plus(f"{self.key}!={self.condition}")


class Exists(Search):
    def expression(self) -> str:
        return urllib.parse.quote_plus(self.key)


class NotExists(Search):
    def expression(self) -> str:
        return urllib.parse.quote_plus(f"!{self.key}")


class RegexMatch(Search):
    condition: str

    def expression(self) -> str:
        return urllib.parse.quote_plus(f"{self.key}={self.condition}")


class LessThan(Search):
    condition: str

    def expression(self) -> str:
        return urllib.parse.quote_plus(f"{self.key}<{self.condition}")


class LessThanEq(Search):
    condition: str

    def expression(self) -> str:
        return urllib.parse.quote_plus(f"{self.key}<={self.condition}")


class GreaterThan(Search):
    condition: str

    def expression(self) -> str:
        return urllib.parse.quote_plus(f"{self.key}>{self.condition}")


class GreaterThanEq(Search):
    condition: str

    def expression(self) -> str:
        return urllib.parse.quote_plus(f"{self.key}>={self.condition}")
