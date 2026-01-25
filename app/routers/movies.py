from fastapi import APIRouter, HTTPException, Response

from app.repository import Repository
from app.models import MovieBase, MovieDetail, RatingCreate

from collections import defaultdict

router = APIRouter()

@router.get("/movies", response_model=list[MovieDetail])
def get_movies(skip: int = 0, limit: int = 10):
    movies = Repository.fetch_all(
        "SELECT * FROM movies LIMIT %s OFFSET %s", 
        (limit, skip)
    )
    
    if not movies:
        return []
    
    movie_ids = [m['id'] for m in movies]
    placeholders = ','.join(['%s'] * len(movie_ids))

    genres_data = Repository.fetch_all(f"""
        SELECT mg.movie_id, mg.genre_name 
        FROM movie_genres mg 
        WHERE mg.movie_id IN ({placeholders})
    """, movie_ids)
    
    cast_data = Repository.fetch_all(f"""
        SELECT c.movie_id, p.id, p.name, p.gender, p.profile_path, 
               c.character_name, c.order_index
        FROM people p
        JOIN cast_members c ON p.id = c.person_id
        WHERE c.movie_id IN ({placeholders})
        ORDER BY c.movie_id, c.order_index
    """, movie_ids)
    
    crew_data = Repository.fetch_all(f"""
        SELECT c.movie_id, p.id, p.name, p.gender, p.profile_path, 
               c.job, c.department
        FROM people p
        JOIN crew_members c ON p.id = c.person_id
        WHERE c.movie_id IN ({placeholders})
    """, movie_ids)
    
    genres_by_movie = defaultdict(list)
    cast_by_movie = defaultdict(list)
    crew_by_movie = defaultdict(list)
    
    for g in genres_data:
        genres_by_movie[g['movie_id']].append(g['genre_name'])
    
    for c in cast_data:
        movie_id = c.pop('movie_id')
        cast_by_movie[movie_id].append(c)
    
    for c in crew_data:
        movie_id = c.pop('movie_id')
        crew_by_movie[movie_id].append(c)
    
    for movie in movies:
        movie_id = movie['id']
        movie['genres'] = genres_by_movie[movie_id]
        movie['cast'] = cast_by_movie[movie_id]
        movie['crew'] = crew_by_movie[movie_id]
    return movies

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
    # Check if user already rated
    existing_rating = Repository.fetch_one("""
        SELECT rating FROM ratings 
        WHERE movie_id = %s AND user_id = %s
    """, (movie_id, rating_data.user_id))
    
    # Upsert rating
    query = """
        INSERT INTO ratings (movie_id, user_id, rating) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            rating = VALUES(rating),
            timestamp = CURRENT_TIMESTAMP
    """
    Repository.execute(query, (movie_id, rating_data.user_id, rating_data.rating))
    
    # Get current vote statistics (before this update/insert affects the aggregate if we read directly from movies, 
    # but we need to know if it was an update or insert to adjust properly. 
    # Actually, simpler to just recalculate from movies table knowing if we added a vote or not)
    
    stats = Repository.fetch_one("""
        SELECT 
            vote_average as avg_rating,
            vote_count as vote_count
        FROM movies
        WHERE id = %s
    """, (movie_id,))
    
    current_avg = stats['avg_rating'] or 0
    current_count = stats['vote_count'] or 0
    
    if existing_rating:
        # Update existing vote
        old_rating = existing_rating['rating']
        # Avoid division by zero if count is somehow 0 (shouldn't happen if rating exists)
        effective_count = max(current_count, 1) 
        current_total = current_avg * effective_count
        new_total = current_total - old_rating + rating_data.rating
        vote_average = round(new_total / effective_count, 1)
        vote_count = effective_count
    else:
        # New vote
        current_total = current_avg * current_count
        new_total = current_total + rating_data.rating
        vote_count = current_count + 1
        vote_average = round(new_total / vote_count, 1)

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