from pathlib import Path
from typing import List

import pandas as pd

ROOT_DIR: Path = Path(__file__).parent.parent

def get_only_movie_ids_existing_in_db(cur , df: pd.DataFrame, column_name: str = 'movieId'):
    cur.execute("SELECT movieId FROM movies_db.movies")

    movie_ids: List[int] = [movie_id[0] for movie_id in cur.fetchall()]

    return df[df[column_name].isin(movie_ids)]

def get_only_tmdb_ids_existing_in_db(cur, df: pd.DataFrame, column_name: str = 'id'):
    cur.execute("SELECT tmdbId FROM movies_db.links;")

    tmdb_ids: List[int] = [tmdb_id[0] for tmdb_id in cur.fetchall()]

    return df[df[column_name].isin(tmdb_ids)]


