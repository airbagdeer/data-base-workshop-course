
from fastapi import APIRouter, HTTPException, Response

from app.database import get_db_connection
from app.models import MovieBase, MovieDetail, RatingCreate

router = APIRouter()

@router.get("/movies", response_model=list[MovieBase])
def get_movies(skip: int = 0, limit: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM movies LIMIT %s OFFSET %s"
    cursor.execute(query, (limit, skip))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return movies

@router.get("/movies/{movie_id}", response_model=MovieDetail)
def get_movie_detail(movie_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get movie info
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    
    if not movie:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Get genres
    cursor.execute("""
        SELECT mg.genre_name 
        FROM movie_genres mg 
        WHERE mg.movie_id = %s
    """, (movie_id,))
    genres = cursor.fetchall()
    
    # Get cast
    cursor.execute("""
        SELECT p.id, p.name, p.gender, p.profile_path, c.character_name, c.order_index
        FROM people p
        JOIN cast_members c ON p.id = c.person_id
        WHERE c.movie_id = %s
        ORDER BY c.order_index
    """, (movie_id,))
    cast = cursor.fetchall()
    
    # Get crew
    cursor.execute("""
        SELECT p.id, p.name, p.gender, p.profile_path, c.job, c.department
        FROM people p
        JOIN crew_members c ON p.id = c.person_id
        WHERE c.movie_id = %s
    """, (movie_id,))
    crew = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    movie['genres'] = [g['genre_name'] for g in genres]
    movie['cast'] = cast
    movie['crew'] = crew
    
    return movie

@router.get("/movies/{movie_id}/poster")
def get_movie_poster(movie_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT image FROM movie_posters WHERE movie_id = %s"
    cursor.execute(query, (movie_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not result:
        raise HTTPException(status_code=404, detail="Poster not found")
        
    return Response(content=result[0], media_type="image/jpeg")

@router.post("/movies/{movie_id}/rate")
def rate_movie(movie_id: int, rating_data: RatingCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Check if movie exists
    cursor.execute("SELECT id FROM movies WHERE id = %s", (movie_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Upsert rating (insert or update if user already rated)
    query = """
        INSERT INTO ratings (movie_id, user_id, rating) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            rating = VALUES(rating),
            timestamp = CURRENT_TIMESTAMP
    """
    cursor.execute(query, (movie_id, rating_data.user_id, rating_data.rating))
    conn.commit()
    
    # Recalculate vote_average and vote_count for this movie
    cursor.execute("""
        SELECT 
            AVG(rating) as avg_rating,
            COUNT(*) as vote_count
        FROM ratings
        WHERE movie_id = %s
    """, (movie_id,))
    
    stats = cursor.fetchone()
    vote_average = round(stats['avg_rating'], 1) if stats['avg_rating'] else 0
    vote_count = stats['vote_count'] if stats['vote_count'] else 0
    
    # Update the movies table with new statistics
    cursor.execute("""
        UPDATE movies 
        SET vote_average = %s, vote_count = %s
        WHERE id = %s
    """, (vote_average, vote_count, movie_id))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return {
        "message": "Rating submitted successfully",
        "vote_average": vote_average,
        "vote_count": vote_count
    }


