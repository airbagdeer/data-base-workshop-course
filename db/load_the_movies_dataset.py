from pathlib import Path

import pandas as pd

from db import ROOT_DIR
from utils import get_only_movie_ids_existing_in_db, get_only_tmdb_ids_existing_in_db

the_movies_dataset_path = ROOT_DIR.joinpath('data/the-movies-dataset')

def load_tmd_movies(conn, cur):
    # TODO: ask Itay if I should also read vote_average and vote_count, also ask maybe we should just use this dataset and that's it.
    movies_metadata = pd.read_csv(the_movies_dataset_path.joinpath('movies_metadata.csv'),
                                  usecols=['id', 'budget', 'original_language', 'original_title', 'overview', 'release_date', 'revenue', 'runtime', 'title']
                                  )

    # TODO: Doesnt work
    movies_metadata['id'] = movies_metadata['id'].astype(int)

    # TODO: movies_metadata is empty after this function
    movies_metadata = get_only_tmdb_ids_existing_in_db(cur, movies_metadata, 'id')

    # Convert values to integer:
    movies_metadata['movieId'] = pd.to_numeric(movies_metadata['id'], errors='coerce')
    movies_metadata.dropna(subset=['movieId'], inplace=True)
    movies_metadata['movieId'] = movies_metadata['movieId'].astype(int)
    movies_metadata.drop_duplicates(subset=['movieId'], inplace=True)
    movies_metadata_no_nans = movies_metadata.astype(object).where(pd.notna(movies_metadata), None)


    # Define the exact order of columns to match the INSERT statement
    column_order = ['movieId', 'budget', 'original_language', 'original_title', 'overview', 'release_date',
                    'revenue', 'runtime', 'title']

    insert_tmd_movies_metadata_query = "INSERT INTO tmd_movies_metadata (movieId, budget, original_language, original_title, overview, release_date, revenue, runtime, title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.executemany(insert_tmd_movies_metadata_query, movies_metadata_no_nans[:100000][column_order].values.tolist())

    conn.commit()
