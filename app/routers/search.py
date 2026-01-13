from fastapi import APIRouter, Query

from app.repository import Repository
from app.models import MovieBase

router = APIRouter()

@router.get("/search", response_model=list[MovieBase])
def search_movies(q: str = Query(..., min_length=3)):
    query = "SELECT * FROM movies WHERE title LIKE %s"
    return Repository.fetch_all(query, (f"%{q}%",))