from typing import Optional, List

from pydantic import BaseModel


class PageQuery(BaseModel):
    limit: Optional[int]
    page: Optional[int]
    offset: Optional[int]

    def page_query(self) -> List[str]:
        limit = f"limit={self.limit}" if self.limit else ""
        page = f"page={self.page}" if self.page else ""
        offset = f"offset={self.offset}" if self.offset else ""
        return [e for e in (limit, page, offset) if e]
