import pandas as pd
from utils import get_only_movie_ids_existing_in_db

movies_amount_limit = 100


def load_movielens(conn, cur):
    load_ml_movies(conn, cur)
    load_ml_ratings(conn, cur)
    load_ml_links(conn, cur)
    load_ml_genome_tags(conn, cur)
    load_ml_genome_scores(conn, cur)
    load_ml_tags(conn, cur)

def load_ml_movies(conn, cur):
    ml_movies = pd.read_csv('../data/ml-latest/movies.csv')
    movies_subset = ml_movies[:movies_amount_limit]
    insert_ml_movies_query = "INSERT INTO ml_movies (movieId, title, genres) VALUES (%s, %s, %s)"
    cur.executemany(insert_ml_movies_query, movies_subset.values.tolist())

    conn.commit()
    pass

def load_ml_ratings(conn, cur):
    ml_ratings = pd.read_csv('../data/ml-latest/ratings.csv')
    ml_ratings = get_only_movie_ids_existing_in_db(cur, ml_ratings, 'movieId')

    ml_ratings['rating_time'] = pd.to_datetime(ml_ratings['timestamp'], unit='s')
    # ml_ratings['rating_time'] = ml_ratings['rating_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    ml_ratings = ml_ratings.drop(columns=['timestamp'])
    insert_ml_ratings_query = "INSERT INTO ml_ratings (userId, movieId, rating , rating_time) Values (%s, %s, %s, %s)"

    # TODO: Change so it doesnt just load the first 100000, (takes too long)
    batch_size = 100000
    for i in range(0, len(ml_ratings), batch_size):
        cur.executemany(insert_ml_ratings_query, ml_ratings.values.tolist()[i:i + batch_size])

    # cur.executemany(insert_ml_ratings_query, ml_ratings.values.tolist()[:batch_size])
    # cur.executemany(insert_ml_ratings_query, ml_ratings.values.tolist())
    conn.commit()

def load_ml_links(conn, cur):
    cur = connection.cursor()
    ml_links = pd.read_csv('../data/ml-latest/links.csv')
    ml_links = get_only_movie_ids_existing_in_db(cur, ml_links)
    ml_links_no_nans = ml_links.astype(object).where(pd.notna(ml_links), None)

    insert_ml_links_query = "INSERT INTO ml_links (movieId, imdbId, tmdbId) VALUES (%s, %s, %s)"
    cur.executemany(insert_ml_links_query, ml_links_no_nans.values.tolist())

    conn.commit()

def load_ml_genome_tags(conn, cur):
    ml_genome_tags = pd.read_csv('../data/ml-latest/genome-tags.csv')
    insert_ml_genome_tags_query = "INSERT INTO ml_genome_tags (tagId, tag) VALUES (%s, %s)"
    cur.executemany(insert_ml_genome_tags_query, ml_genome_tags.values.tolist())

    conn.commit()

def load_ml_genome_scores(conn, cur):
    ml_genome_scores = pd.read_csv('../data/ml-latest/genome-scores.csv')

    insert_ml_genome_scores_query = "INSERT INTO ml_genome_scores (movieId, tagId, relevance) VALUES (%s, %s, %s)"
    data = ml_genome_scores.values.tolist()
    batch_size = 100000

    # TODO: putting only 100000 inside the
    cur.executemany(insert_ml_genome_scores_query, data[:batch_size])
    conn.commit()
    # for i in range(0, len(data), batch_size):
    #     cur.executemany(insert_ml_genome_scores_query, data[i:i+batch_size])
    #     conn.commit()

    # cur.executemany(insert_ml_genome_scores_query, ml_genome_scores.values.tolist())

    # conn.commit()


def load_ml_tags(conn, cur):
    ml_tags = pd.read_csv('../data/ml-latest/tags.csv')

    ml_tags['tag_time'] = pd.to_datetime(ml_tags['timestamp'], unit='s')
    ml_tags = ml_tags.drop(columns=['timestamp'])

    insert_ml_tags_query = "INSERT INTO ml_tags (userId, movieId, tag , tag_time) Values (%s, %s, %s, %s)"

    # TODO: Change so it doesnt just load the first 100000, (takes too long)
    batch_size = 100000
    # for i in range(0, len(ml_tags), batch_size):
    #     cur.executemany(insert_ml_tags_query, ml_tags.values.tolist()[i:i + batch_size])

    cur.executemany(insert_ml_tags_query, ml_tags.values.tolist()[:batch_size])

    conn.commit()

