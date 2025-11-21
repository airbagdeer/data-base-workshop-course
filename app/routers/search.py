from fastapi import APIRouter, Query
from typing import List
from app.database import get_db_connection
from app.models import MovieBase

router = APIRouter()

@router.get("/search", response_model=List[MovieBase])
def search_movies(q: str = Query(..., min_length=3)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM movies WHERE title LIKE %s"
    cursor.execute(query, (f"%{q}%",))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return movies
