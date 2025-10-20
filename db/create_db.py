from generate_schema import generate_schema
from load_movielens import load_movielens
from load_the_movies_dataset import load_tmd_movies
from connect_to_db import connect_to_db

def main():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        generate_schema(conn)
        print(f'Generated Schema ...')
        load_movielens(conn, cur)
        print(f'Loaded MovieLens Data Set ...')
        load_tmd_movies(conn, cur)
        print(f'Loaded The Movies Data Set ...')
    except Exception as e:
        print(f'Error in Creating The Data Base: {e}')

    

if __name__ == "__main__":
    main()