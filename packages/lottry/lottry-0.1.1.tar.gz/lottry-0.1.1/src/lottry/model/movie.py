from pydantic import BaseModel


class Movie(BaseModel):
    _id: str
    name: str
    runtimeInMinutes: int
    budgetInMillions: int
    boxOfficeRevenueInMillions: int
    academyAwardNominations: int
    academyAwardWins: int
    rottenTomatoesScore: int