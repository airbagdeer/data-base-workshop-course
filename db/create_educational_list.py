import ast
import json
import os

import pandas as pd


def get_genres(x):
    try:
        return [g['name'] for g in ast.literal_eval(x)]
    except:
        return []

educational_movies_ids = ['tt0268978', 'tt2980516', 'tt2084970', 'tt0787524', 'tt1385956', 'tt6223974', 'tt0118889', 'tt0112384', 'tt1213641', 'tt0086197', 'tt0132477', 'tt3659388', 'tt0118884', 'tt2543164', 'tt0138704', 'tt0390384', 'tt0816692', 'tt1454468', 'tt0995036', 'tt0395571', 'tt6700846', 'tt11394170', 'tt11464826', 'tt4736550', 'tt0470752', 'tt1798709', 'tt3774114', 'tt0086567', 'tt0113243', 'tt4044364', 'tt2084953', 'tt5275828', 'tt3268458', 'tt2119396', 'tt0084827', 'tt1677720', 'tt2177843', 'tt0315417', 'tt1596363', 'tt1645089', 'tt1615147', 'tt1210166', 'tt1016268', 'tt1742683', 'tt5723056', 'tt1152822', 'tt1358383', 'tt6438096', 'tt9351980', 'tt4276820', 'tt0256408', 'tt1737747', 'tt3762912', 'tt6185286', 'tt2215151', 'tt5895028', 'tt0074119', 'tt1895587', 'tt6294822', 'tt0317910', 'tt0395169', 'tt0108052', 'tt0253474', 'tt2375605', 'tt3521134', 'tt0912593', 'tt1559549', 'tt0361596', 'tt0436971', 'tt1085507', 'tt4935110', 'tt11382384', 'tt17041964', 'tt4908644', 'tt0420293', 'tt7664504', 'tt11668320', 'tt0219822', 'tt7775622', 'tt0379557', 'tt7286916', 'tt1155592', 'tt1772925', 'tt0847817', 'tt1587707', 'tt0024088', 'tt3810760', 'tt0770802', 'tt1598778', 'tt5686132', 'tt0453533', 'tt3741860', 'tt12888462', 'tt2382298', 'tt12922082', 'tt2545118', 'tt1567233', 'tt5541848', 'tt1286537', 'tt0390521', 'tt1227378', 'tt5239942', 'tt1229367', 'tt0386032', 'tt0497116', 'tt6322922', 'tt5929776', 'tt14539726', 'tt1579361', 'tt6333054', 'tt8618654', 'tt2224026', 'tt0072000', 'tt0358456', 'tt0492931', 'tt5203824', 'tt14152756', 'tt3302820', 'tt8969332', 'tt9114472', 'tt0099158', 'tt3455224', 'tt1566648', 'tt6276272', 'tt0318202', 'tt7215232', 'tt7153434', 'tt10711654', 'tt1437364', 'tt6588332', 'tt0144255', 'tt2008513', 'tt0090015', 'tt7905466', 'tt0185016', 'tt0048434', 'tt0846011', 'tt0465589', 'tt4515578']


def create_list():
    print("Reading movies_metadata.csv...")
    df = pd.read_csv('data/the-movies-dataset/movies_metadata.csv', low_memory=False)
    
    # Filter educational movies
    print("Filtering movies...")
    educational_movies = []
    
    poster_dir = 'data/posterlens/covers/covers/'

    # Filter educational movies by IDs
    df = df[df['imdb_id'].isin(educational_movies_ids)]
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
