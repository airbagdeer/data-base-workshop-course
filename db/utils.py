import pandas as pd

from db import cur


def check_table_exists(table_name: str) -> bool:
    cur.execute("SHOW TABLES LIKE %s", (table_name,))
    table_exists = cur.fetchone()

    table_nonempty = False
    if table_exists:
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cur.fetchone()[0]
        table_nonempty = row_count > 0

    return bool(table_exists and table_nonempty)


def get_only_movie_ids_existing_in_db(df: pd.DataFrame, column_name: str = 'movieId'):
    cur.execute("SELECT movieId FROM movies.ml_movies")

    movie_ids = [movie_id[0] for movie_id in cur.fetchall()]

    return df[df[column_name].isin(movie_ids)]
