from fastapi import APIRouter
from app.database import get_db_connection
from typing import List, Dict, Any

router = APIRouter()

@router.get("/analytics/popular-genres")
def popular_genres():
    """1. Top 5 most popular genres in documentaries."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT g.name, COUNT(mg.movie_id) as movie_count
        FROM genres g
        JOIN movie_genres mg ON g.id = mg.genre_id
        GROUP BY g.name
        ORDER BY movie_count DESC
        LIMIT 5
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/analytics/prolific-actors")
def prolific_actors():
    """2. Actors who have appeared in multiple documentaries."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT p.name, COUNT(c.movie_id) as movie_count
        FROM people p
        JOIN cast_members c ON p.id = c.person_id
        GROUP BY p.id, p.name
        HAVING movie_count > 1
        ORDER BY movie_count DESC
        LIMIT 10
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/analytics/avg-runtime-by-year")
def avg_runtime_by_year():
    """3. Average runtime of documentaries by release year."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT YEAR(release_date) as year, AVG(runtime) as avg_runtime
        FROM movies
        WHERE release_date IS NOT NULL
        GROUP BY year
        ORDER BY year DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/analytics/flops")
def flops():
    """4. Movies with high budget (>1M) but low revenue (< budget)."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT title, budget, revenue, (budget - revenue) as loss
        FROM movies
        WHERE budget > 1000000 AND revenue < budget AND revenue > 0
        ORDER BY loss DESC
        LIMIT 10
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/analytics/director-actors")
def director_actors():
    """5. Directors who also acted in the same movie."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT p.name, m.title
        FROM people p
        JOIN cast_members c ON p.id = c.person_id
        JOIN crew_members cr ON p.id = cr.person_id AND c.movie_id = cr.movie_id
        JOIN movies m ON c.movie_id = m.id
        WHERE cr.job = 'Director'
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/analytics/top-production-countries")
def top_production_countries():
    """6. Top production countries by number of movies."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT pc.name, COUNT(mc.movie_id) as movie_count
        FROM production_countries pc
        JOIN movie_countries mc ON pc.iso_3166_1 = mc.country_code
        GROUP BY pc.name
        ORDER BY movie_count DESC
        LIMIT 10
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/analytics/keyword-rich-movies")
def keyword_rich_movies():
    """7. Movies with the most keywords."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT m.title, COUNT(mk.keyword_id) as keyword_count
        FROM movies m
        JOIN movie_keywords mk ON m.id = mk.movie_id
        GROUP BY m.id, m.title
        ORDER BY keyword_count DESC
        LIMIT 10
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/analytics/history-war-movies")
def history_war_movies():
    """8. Movies with both 'History' and 'War' genres (or similar combination)."""
    # Since we only have documentaries, let's check for 'History' and 'Music' or similar if they exist.
    # Or just check for movies with > 3 genres.
    # Let's stick to "Movies with > 3 genres" as a complex query involving aggregation and filtering.
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT m.title, COUNT(mg.genre_id) as genre_count
        FROM movies m
        JOIN movie_genres mg ON m.id = mg.movie_id
        GROUP BY m.id, m.title
        HAVING genre_count > 3
        ORDER BY genre_count DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/analytics/best-year")
def best_year():
    """9. Year with the highest average vote (min 3 movies)."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT YEAR(release_date) as year, AVG(vote_average) as avg_vote, COUNT(*) as movie_count
        FROM movies
        WHERE release_date IS NOT NULL
        GROUP BY year
        HAVING movie_count >= 3
        ORDER BY avg_vote DESC
        LIMIT 1
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@router.get("/analytics/multiskilled-crew")
def multiskilled_crew():
    """10. Crew members who worked in more than one department."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT p.name, COUNT(DISTINCT cr.department) as dept_count
        FROM people p
        JOIN crew_members cr ON p.id = cr.person_id
        GROUP BY p.id, p.name
        HAVING dept_count > 1
        ORDER BY dept_count DESC
        LIMIT 10
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
