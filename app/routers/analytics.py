from fastapi import APIRouter
from app.repository import Repository

router = APIRouter()

@router.get("/analytics/popular-genres")
def popular_genres():
    """1. Top 5 most popular genres in documentaries."""
    query = """
        SELECT genre_name AS genre, COUNT(movie_id) AS movie_count
        FROM movie_genres
        GROUP BY genre_name
        ORDER BY movie_count DESC
        LIMIT 5;
    """
    return Repository.fetch_all(query)

@router.get("/analytics/top-actors")
def prolific_actors():
    """2. Actors who have appeared in multiple documentaries."""
    query = """
        SELECT p.name as actor_name, COUNT(c.movie_id) as movie_count
        FROM people p
        JOIN cast_members c ON p.id = c.person_id
        GROUP BY p.id, p.name
        HAVING movie_count > 1
        ORDER BY movie_count DESC
        LIMIT 10
    """
    return Repository.fetch_all(query)

@router.get("/analytics/average-runtime-by-genre")
def avg_runtime_by_genre():
    """3. Average runtime of documentaries by genre."""
    query = """
        SELECT mg.genre_name AS genre, AVG(m.runtime) AS avg_runtime
        FROM movie_genres mg
        JOIN movies m ON mg.movie_id = m.id
        WHERE m.runtime IS NOT NULL
        GROUP BY mg.genre_name
        ORDER BY avg_runtime DESC
        LIMIT 10
    """
    return Repository.fetch_all(query)

@router.get("/analytics/flops")
def flops():
    """4. Movies with high budget (>1M) but low revenue (< budget)."""
    query = """
        SELECT title, budget, revenue, (budget - revenue) as loss
        FROM movies
        WHERE budget > 1000000 AND revenue < budget AND revenue > 0
        ORDER BY loss DESC
        LIMIT 10
    """
    return Repository.fetch_all(query)

@router.get("/analytics/director-actors")
def director_actors():
    """5. Directors who also acted in the same movie."""
    query = """
        SELECT p.name, m.title
        FROM people p
        JOIN cast_members c ON p.id = c.person_id
        JOIN crew_members cr ON p.id = cr.person_id AND c.movie_id = cr.movie_id
        JOIN movies m ON c.movie_id = m.id
        WHERE cr.job = 'Director'
    """
    return Repository.fetch_all(query)

@router.get("/analytics/top-production-countries")
def top_production_countries():
    """6. Top production countries by number of movies."""
    query = """
        SELECT pc.name, COUNT(mc.movie_id) as movie_count
        FROM production_countries pc
        JOIN movie_countries mc ON pc.iso_3166_1 = mc.country_code
        GROUP BY pc.name
        ORDER BY movie_count DESC
        LIMIT 10
    """
    return Repository.fetch_all(query)

@router.get("/analytics/keyword-rich-movies")
def keyword_rich_movies():
    """7. Movies with the most keywords."""
    query = """
        SELECT m.title, COUNT(mk.keyword_id) as keyword_count
        FROM movies m
        JOIN movie_keywords mk ON m.id = mk.movie_id
        GROUP BY m.id, m.title
        ORDER BY keyword_count DESC
        LIMIT 10
    """
    return Repository.fetch_all(query)

@router.get("/analytics/history-war-movies")
def history_war_movies():
    """8. Movies with both 'History' and 'War' genres (or similar combination)."""
    query = """
        SELECT m.title, COUNT(mg.genre_name) as genre_count
        FROM movies m
        JOIN movie_genres mg ON m.id = mg.movie_id
        GROUP BY m.id, m.title
        HAVING genre_count > 3
        ORDER BY genre_count DESC
    """
    return Repository.fetch_all(query)

@router.get("/analytics/best-year")
def best_year():
    """9. Year with the highest average vote (min 3 movies)."""
    query = """
        SELECT YEAR(release_date) as year, AVG(vote_average) as avg_vote, COUNT(*) as movie_count
        FROM movies
        WHERE release_date IS NOT NULL
        GROUP BY year
        HAVING movie_count >= 3
        ORDER BY avg_vote DESC
        LIMIT 1
    """
    return Repository.fetch_all(query)

@router.get("/analytics/multiskilled-crew")
def multiskilled_crew():
    """10. Crew members who worked in more than one department."""
    query = """
        SELECT p.name, COUNT(DISTINCT cr.department) as dept_count
        FROM people p
        JOIN crew_members cr ON p.id = cr.person_id
        GROUP BY p.id, p.name
        HAVING dept_count > 1
        ORDER BY dept_count DESC
        LIMIT 10
    """
    return Repository.fetch_all(query)