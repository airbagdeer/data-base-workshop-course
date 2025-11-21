import pandas as pd
import ast
import os
import json
from pathlib import Path
from db.connect_to_db import connect_to_db

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "the-movies-dataset"
POSTERS_DIR = BASE_DIR / "data" / "posterlens" / "covers" / "covers"
EDUCATIONAL_LIST_PATH = BASE_DIR / "data" / "educational_movies.json"

def parse_json_safe(x):
    try:
        return ast.literal_eval(x)
    except (ValueError, SyntaxError):
        return []

def get_poster_filename(movie_id):
    return f"{int(movie_id):07d}.jpg"

def load_data():
    print("Connecting to database...")
    conn = connect_to_db()
    cursor = conn.cursor()

    # 1. Re-create Schema
    print("Re-creating schema...")
    with open(BASE_DIR / "db" / "new_schema.sql", "r") as f:
        schema_sql = f.read()
        # Split by semi-colon to execute multiple statements
        statements = schema_sql.split(';')
        for statement in statements:
            if statement.strip():
                # print(f"Executing: {statement[:50]}...")
                cursor.execute(statement)
    conn.commit()

    # 2. Load Movies Metadata
    print("Loading movies metadata...")
    movies_df = pd.read_csv(DATA_DIR / "movies_metadata.csv", low_memory=False)
    
    # Load Educational Movies List
    print(f"Loading educational movies list from {EDUCATIONAL_LIST_PATH}...")
    with open(EDUCATIONAL_LIST_PATH, "r") as f:
        educational_ids = json.load(f)
        
    # Take top 100
    target_ids = educational_ids[:100]
    print(f"Targeting top {len(target_ids)} educational movies.")
    
    # Filter movies_df
    movies_df['id'] = pd.to_numeric(movies_df['id'], errors='coerce')
    movies_df = movies_df.dropna(subset=['id'])
    movies_df['id'] = movies_df['id'].astype(int)
    
    movies_df = movies_df[movies_df['id'].isin(target_ids)]
    
    # Sort to match the order in target_ids (popularity desc)
    movies_df = movies_df.set_index('id').reindex(target_ids).reset_index()
    
    print(f"Found {len(movies_df)} movies in metadata.")

    # Load Credits and Keywords
    print("Loading credits and keywords...")
    credits_df = pd.read_csv(DATA_DIR / "credits.csv")
    keywords_df = pd.read_csv(DATA_DIR / "keywords.csv")
    
    # Convert IDs to int for merging
    credits_df['id'] = pd.to_numeric(credits_df['id'], errors='coerce').fillna(0).astype(int)
    keywords_df['id'] = pd.to_numeric(keywords_df['id'], errors='coerce').fillna(0).astype(int)

    # Prepare Insert Statements
    insert_movie = """
        INSERT INTO movies (id, title, original_title, overview, release_date, runtime, budget, revenue, popularity, vote_average, vote_count, status, tagline)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE title=VALUES(title)
    """
    
    insert_genre = "INSERT IGNORE INTO genres (id, name) VALUES (%s, %s)"
    insert_movie_genre = "INSERT IGNORE INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)"
    
    insert_person = "INSERT IGNORE INTO people (id, name, gender, profile_path) VALUES (%s, %s, %s, %s)"
    insert_cast = "INSERT IGNORE INTO cast_members (credit_id, movie_id, person_id, character_name, order_index) VALUES (%s, %s, %s, %s, %s)"
    insert_crew = "INSERT IGNORE INTO crew_members (credit_id, movie_id, person_id, job, department) VALUES (%s, %s, %s, %s, %s)"
    
    insert_keyword = "INSERT IGNORE INTO keywords (id, name) VALUES (%s, %s)"
    insert_movie_keyword = "INSERT IGNORE INTO movie_keywords (movie_id, keyword_id) VALUES (%s, %s)"
    
    insert_company = "INSERT IGNORE INTO production_companies (id, name) VALUES (%s, %s)"
    insert_movie_company = "INSERT IGNORE INTO movie_companies (movie_id, company_id) VALUES (%s, %s)"
    
    insert_country = "INSERT IGNORE INTO production_countries (iso_3166_1, name) VALUES (%s, %s)"
    insert_movie_country = "INSERT IGNORE INTO movie_countries (movie_id, country_code) VALUES (%s, %s)"
    
    insert_language = "INSERT IGNORE INTO spoken_languages (iso_639_1, name) VALUES (%s, %s)"
    insert_movie_language = "INSERT IGNORE INTO movie_languages (movie_id, language_code) VALUES (%s, %s)"
    
    insert_poster = "INSERT INTO movie_posters (movie_id, image) VALUES (%s, %s) ON DUPLICATE KEY UPDATE image=VALUES(image)"

    count = 0
    for _, row in movies_df.iterrows():
        movie_id = row['id']
        
        # Insert Movie
        # Handle NaN/None for SQL
        def clean(val, default=None):
            if pd.isna(val): return default
            return val

        cursor.execute(insert_movie, (
            movie_id,
            clean(row['title']),
            clean(row['original_title']),
            clean(row['overview']),
            clean(row['release_date']),
            clean(row['runtime']),
            clean(row['budget'], 0),
            clean(row['revenue'], 0),
            clean(row['popularity'], 0.0),
            clean(row['vote_average'], 0.0),
            clean(row['vote_count'], 0),
            clean(row['status']),
            clean(row['tagline'])
        ))
        
        # Genres
        genres = parse_json_safe(row['genres'])
        for g in genres:
            cursor.execute(insert_genre, (g['id'], g['name']))
            cursor.execute(insert_movie_genre, (movie_id, g['id']))
            
        # Production Companies
        companies = parse_json_safe(row['production_companies'])
        for c in companies:
            cursor.execute(insert_company, (c['id'], c['name']))
            cursor.execute(insert_movie_company, (movie_id, c['id']))
            
        # Production Countries
        countries = parse_json_safe(row['production_countries'])
        for c in countries:
            cursor.execute(insert_country, (c['iso_3166_1'], c['name']))
            cursor.execute(insert_movie_country, (movie_id, c['iso_3166_1']))
            
        # Spoken Languages
        languages = parse_json_safe(row['spoken_languages'])
        for l in languages:
            cursor.execute(insert_language, (l['iso_639_1'], l['name']))
            cursor.execute(insert_movie_language, (movie_id, l['iso_639_1']))

        # Credits (Cast & Crew)
        movie_credits = credits_df[credits_df['id'] == movie_id]
        if not movie_credits.empty:
            cast_list = parse_json_safe(movie_credits.iloc[0]['cast'])
            crew_list = parse_json_safe(movie_credits.iloc[0]['crew'])
            
            for member in cast_list:
                cursor.execute(insert_person, (member['id'], member['name'], member.get('gender'), member.get('profile_path')))
                cursor.execute(insert_cast, (member['credit_id'], movie_id, member['id'], member.get('character'), member.get('order')))
                
            for member in crew_list:
                cursor.execute(insert_person, (member['id'], member['name'], member.get('gender'), member.get('profile_path')))
                cursor.execute(insert_crew, (member['credit_id'], movie_id, member['id'], member.get('job'), member.get('department')))

        # Keywords
        movie_keywords = keywords_df[keywords_df['id'] == movie_id]
        if not movie_keywords.empty:
            k_list = parse_json_safe(movie_keywords.iloc[0]['keywords'])
            for k in k_list:
                cursor.execute(insert_keyword, (k['id'], k['name']))
                cursor.execute(insert_movie_keyword, (movie_id, k['id']))
        
        # Poster
        poster_filename = get_poster_filename(movie_id)
        poster_path = POSTERS_DIR / poster_filename
        if poster_path.exists():
            with open(poster_path, "rb") as f:
                image_data = f.read()
                cursor.execute(insert_poster, (movie_id, image_data))
        
        count += 1
        if count % 10 == 0:
            print(f"Processed {count} movies...")
            conn.commit()

    conn.commit()
    cursor.close()
    conn.close()
    print("Data loading complete!")

if __name__ == "__main__":
    load_data()
