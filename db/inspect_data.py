import pandas as pd
import os

def inspect():
    print("--- movies_metadata.csv columns ---")
    try:
        df = pd.read_csv('data/the-movies-dataset/movies_metadata.csv', nrows=5)
        print(df.columns.tolist())
        print(df[['id', 'imdb_id']].head())
    except Exception as e:
        print(f"Error reading metadata: {e}")

    print("\n--- Poster filenames ---")
    try:
        poster_dir = 'data/posterlens/covers/covers/'
        files = os.listdir(poster_dir)
        print(files[:10])
    except Exception as e:
        print(f"Error listing posters: {e}")

if __name__ == "__main__":
    inspect()
