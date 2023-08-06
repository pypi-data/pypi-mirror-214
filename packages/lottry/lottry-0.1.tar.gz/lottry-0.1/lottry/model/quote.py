from pydantic import BaseModel


class Quote(BaseModel):
    _id: str
    dialog: str
    movie: str
    character: str
    id: str
