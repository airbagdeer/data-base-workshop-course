import ast
import json
import os

import pandas as pd


def get_genres(x):
    try:
        return [g['name'] for g in ast.literal_eval(x)]
    except:
        return []

educational_movies_ids = [453, 266856, 205596, 353326, 202141, 436305, 124818, 568, 369972, 9549, 13466, 286217, 686, 329865, 473, 14337, 157336, 49047, 15044, 34843, 455008, 653734, 656690, 566222, 264660, 152601, 302401, 860, 10428, 293310, 159622, 360030, 250658, 80787, 97, 333339, 97690, 45049, 318846, 44639, 50839, 60308, 13020, 65034, 603106, 43942, 31869, 438137, 521005, 565716, 310307, 14268, 61854, 385805, 483010, 159008, 407806, 891, 314365, 446354, 12698, 205, 424, 423, 123678, 267480, 12901, 39312, 1777, 14286, 15912, 356201, 653746, 926676, 355020, 308032, 489988, 682589, 1278955, 441, 515042, 11194, 489471, 14048, 80767, 13348, 39452, 664403, 405362, 392553, 89708, 39538, 424600, 10085, 290504, 682110, 250766, 796759, 158999, 64288, 415086, 18570, 9372, 72914, 458991, 30849, 2359, 935238, 1781, 432602, 410718, 828146, 84185, 432615, 737157, 228161, 54805, 30238, 4832, 431339, 801058, 282297, 543084, 599379, 15087, 263614, 39440, 899632, 5168, 592983, 493121, 648510, 65103, 477837, 292006, 89874, 42044, 543580, 1109979, 661805, 362888, 803, 204291, 547545, 1511545, 276477, 96955, 1262786, 341338, 253724]


def create_list():
    print("Reading movies_metadata.csv...")
    df = pd.read_csv('data/the-movies-dataset/movies_metadata.csv', low_memory=False)
    
    # Filter educational movies
    print("Filtering movies...")
    educational_movies = []
    
    poster_dir = 'data/posterlens/covers/covers/'

    # Filter educational movies by IDs
    df = df[df['id'].isin(educational_movies_ids)]
    print(f"Found {len(df)} educational movies in the dataset.")

    for index, row in df.iterrows():
        try:
            imdb_id = str(row['imdb_id'])
            
            if imdb_id.startswith('tt'):
                numeric_id = imdb_id[2:] # Remove 'tt'
                poster_filename = f"{numeric_id}.jpg"
                poster_path = os.path.join(poster_dir, poster_filename)
                
                if os.path.exists(poster_path):
                    educational_movies.append({
                        'id': row['id'],
                        'title': row['title'],
                        'imdb_id': imdb_id,
                        'poster_file': poster_filename,
                        'popularity': float(row['popularity']) if pd.notnull(row['popularity']) else 0
                        })
        except Exception:
            continue
            
    # Sort by popularity
    print(f"Found {len(educational_movies)} educational movies with posters.")
    educational_movies.sort(key=lambda x: x['popularity'], reverse=True)
    
    # Take top 200
    top_200 = educational_movies[:200]
    
    # Save to JSON
    with open('data/educational_movies.json', 'w') as f:
        json.dump(top_200, f, indent=2)
        
    print(f"Saved top {len(top_200)} movies to data/educational_movies.json")

if __name__ == "__main__":
    create_list()
