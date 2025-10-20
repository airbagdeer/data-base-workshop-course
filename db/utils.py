import pandas as pd

def get_only_movie_ids_existing_in_db(cur, df: pd.DataFrame, column_name: str = 'movieId'):
    cur.execute("SELECT movieId FROM movies.ml_movies")

    movie_ids = [movie_id[0] for movie_id in cur.fetchall()]

    return df[df[column_name].isin(movie_ids)]
