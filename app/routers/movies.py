from fastapi import APIRouter, HTTPException, Response

from app.repository import Repository
from app.models import MovieBase, MovieDetail, RatingCreate

router = APIRouter()

@router.get("/movies", response_model=list[MovieBase])
def get_movies(skip: int = 0, limit: int = 10):
    query = "SELECT * FROM movies LIMIT %s OFFSET %s"
    return Repository.fetch_all(query, (limit, skip))

@router.get("/movies/{movie_id}", response_model=MovieDetail)
def get_movie_detail(movie_id: int):
    # Get movie info
    movie = Repository.fetch_one("SELECT * FROM movies WHERE id = %s", (movie_id,))
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Get genres
    genres = Repository.fetch_all("""
        SELECT mg.genre_name 
        FROM movie_genres mg 
        WHERE mg.movie_id = %s
    """, (movie_id,))
    
    # Get cast
    cast = Repository.fetch_all("""
        SELECT p.id, p.name, p.gender, p.profile_path, c.character_name, c.order_index
        FROM people p
        JOIN cast_members c ON p.id = c.person_id
        WHERE c.movie_id = %s
        ORDER BY c.order_index
    """, (movie_id,))
    
    # Get crew
    crew = Repository.fetch_all("""
        SELECT p.id, p.name, p.gender, p.profile_path, c.job, c.department
        FROM people p
        JOIN crew_members c ON p.id = c.person_id
        WHERE c.movie_id = %s
    """, (movie_id,))
    
    movie['genres'] = [g['genre_name'] for g in genres]
    movie['cast'] = cast
    movie['crew'] = crew
    
    return movie

@router.get("/movies/{movie_id}/poster")
def get_movie_poster(movie_id: int):
    query = "SELECT image FROM movie_posters WHERE movie_id = %s"
    result = Repository.fetch_one(query, (movie_id,))
    
    if not result:
        raise HTTPException(status_code=404, detail="Poster not found")
        
    return Response(content=result['image'], media_type="image/jpeg")

@router.post("/movies/{movie_id}/rate")
def rate_movie(movie_id: int, rating_data: RatingCreate):
    # Check if movie exists
    movie = Repository.fetch_one("SELECT id FROM movies WHERE id = %s", (movie_id,))
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Upsert rating (insert or update if user already rated)
    query = """
        INSERT INTO ratings (movie_id, user_id, rating) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            rating = VALUES(rating),
            timestamp = CURRENT_TIMESTAMP
    """
    Repository.execute(query, (movie_id, rating_data.user_id, rating_data.rating))
    
    # Get current vote statistics
    stats = Repository.fetch_one("""
        SELECT 
            vote_average as avg_rating,
            vote_count as vote_count
        FROM movies
        WHERE id = %s
    """, (movie_id,))
    
    vote_average = round((stats['avg_rating'] * stats['vote_count'] + rating_data.rating) / (stats['vote_count'] + 1), 1) if (stats['avg_rating'] and stats['vote_count']) else rating_data.rating
    vote_count = stats['vote_count'] + 1 if stats['vote_count'] else 1
    
    # Update the movies table with new statistics
    Repository.execute("""
        UPDATE movies 
        SET vote_average = %s, vote_count = %s
        WHERE id = %s
    """, (vote_average, vote_count, movie_id))
    
    return {
        "message": "Rating submitted successfully",
        "vote_average": vote_average,
        "vote_count": vote_count
    }