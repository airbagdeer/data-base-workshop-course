from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Genre(BaseModel):
    id: int
    name: str

class Person(BaseModel):
    id: int
    name: str
    gender: Optional[int] = None
    profile_path: Optional[str] = None

class CastMember(Person):
    character_name: Optional[str] = None
    order_index: Optional[int] = None

class CrewMember(Person):
    job: Optional[str] = None
    department: Optional[str] = None

class RatingCreate(BaseModel):
    rating: float
    order_index: Optional[int] = None

class MovieBase(BaseModel):
    id: int
    title: str
    original_title: Optional[str] = None
    overview: Optional[str] = None
    release_date: Optional[date] = None
    runtime: Optional[float] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    popularity: Optional[float] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    status: Optional[str] = None
    tagline: Optional[str] = None

class MovieDetail(MovieBase):
    genres: List[Genre] = []
    cast: List[CastMember] = []
    crew: List[CrewMember] = []
