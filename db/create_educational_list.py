import pandas as pd
import json
import os
import ast

def get_genres(x):
    try:
        return [g['name'] for g in ast.literal_eval(x)]
    except:
        return []

def create_list():
    print("Reading movies_metadata.csv...")
    df = pd.read_csv('data/the-movies-dataset/movies_metadata.csv', low_memory=False)
    
    # Filter educational movies
    print("Filtering movies...")
    educational_movies = []
    
    poster_dir = 'data/posterlens/covers/covers/'
    
    for index, row in df.iterrows():
        try:
            genres = get_genres(row['genres'])
            
            # Educational filter: (Documentary OR History) AND NOT Horror
            if ('Documentary' in genres or 'History' in genres) and 'Horror' not in genres:
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
        except Exception as e:
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
