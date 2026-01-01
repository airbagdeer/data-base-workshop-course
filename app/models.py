from datetime import date

from pydantic import BaseModel

class Person(BaseModel):
    id: int
    name: str
    gender: int | None = None
    profile_path: str | None = None

class CastMember(Person):
    character_name: str | None = None
    order_index: int | None = None

class CrewMember(Person):
    job: str | None = None
    department: str | None = None

class RatingCreate(BaseModel):
    rating: float
    order_index: int | None = None

class MovieBase(BaseModel):
    id: int
    title: str
    original_title: str | None = None
    overview: str | None = None
    release_date: date | None = None
    runtime: float | None = None
    budget: int | None = None
    revenue: int | None = None
    popularity: float | None = None
    vote_average: float | None = None
    vote_count: int | None = None
    status: str | None = None
    tagline: str | None = None

class MovieDetail(MovieBase):
    genres: list[str] = []
    cast: list[CastMember] = []
    crew: list[CrewMember] = []
