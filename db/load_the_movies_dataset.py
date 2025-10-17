from pathlib import Path

import pandas as pd

from db import cur, conn, check_table_exists, get_only_movie_ids_existing_in_db

the_movies_dataset_path = Path("../data/the-movies-dataset/")

def load_tmd_movies():
    table_exists = check_table_exists('tmd_movies_metadata')
    # TODO: ask Itay if I should also read vote_average and vote_count, also ask maybe we should just use this dataset and that's it.
    movies_metadata = pd.read_csv(the_movies_dataset_path.joinpath('movies_metadata.csv'),
                                  usecols=['id', 'budget', 'original_language', 'original_title', 'overview', 'release_date', 'revenue', 'runtime', 'title']
                                  )

    movies_metadata = get_only_movie_ids_existing_in_db(movies_metadata, 'id')

    # Convert values to integer:
    movies_metadata['movieId'] = pd.to_numeric(movies_metadata['id'], errors='coerce')
    movies_metadata.dropna(subset=['movieId'], inplace=True)
    movies_metadata['movieId'] = movies_metadata['movieId'].astype(int)
    movies_metadata.drop_duplicates(subset=['movieId'], inplace=True)
    movies_metadata_no_nans = movies_metadata.astype(object).where(pd.notna(movies_metadata), None)

    if not table_exists:
        create_tmd_movies_metadata_table_query = """
        CREATE TABLE IF NOT EXISTS tmd_movies_metadata(
            movieId INT PRIMARY KEY,
            budget BIGINT,
            original_language VARCHAR(2),
            original_title VARCHAR(500),
            overview VARCHAR(10000),
            release_date DATE,
            revenue BIGINT,
            runtime INT,
            title VARCHAR(500))
        """

        cur.execute(create_tmd_movies_metadata_table_query)

        # Define the exact order of columns to match the INSERT statement
        column_order = ['movieId', 'budget', 'original_language', 'original_title', 'overview', 'release_date',
                        'revenue', 'runtime', 'title']

        insert_tmd_movies_metadata_query = "INSERT INTO tmd_movies_metadata (movieId, budget, original_language, original_title, overview, release_date, revenue, runtime, title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.executemany(insert_tmd_movies_metadata_query, movies_metadata_no_nans[:100000][column_order].values.tolist())

        conn.commit()


load_tmd_movies()
