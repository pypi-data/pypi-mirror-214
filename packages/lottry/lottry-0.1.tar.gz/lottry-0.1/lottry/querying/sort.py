from pydantic import BaseModel


class Sort(BaseModel):
    def expression(self) -> str:
        ...


class SortAsc(Sort):
    key: str

    def expression(self) -> str:
        return f"sort={self.key}:asc"


class SortDesc(Sort):
    key: str

    def expression(self) -> str:
        return f"sort={self.key}:desc"
