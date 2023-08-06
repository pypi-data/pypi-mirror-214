from typing import List, Optional, Union

from pydantic import BaseModel

from lottry.model.movie import Movie
from lottry.model.quote import Quote

Entity = Union[Movie, Quote]


class ApiResponse(BaseModel):
    docs: List[Entity]
    total: Optional[int]
    offset: Optional[int]
    limit: Optional[int]
    page: Optional[int]
    pages: Optional[int]


class Page(BaseModel):
    total: Optional[int]
    offset: Optional[int]
    limit: Optional[int]
    page: Optional[int]
    pages: Optional[int]


class PagedResource(BaseModel):
    docs: List[Entity]
    pagination: Page
