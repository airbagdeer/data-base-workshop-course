CREATE TABLE IF NOT EXISTS movies(
            movieId INT PRIMARY KEY,
            title VARCHAR(500),
            genres VARCHAR(500)
);


CREATE TABLE IF NOT EXISTS ratings(
            userId INT,
            movieId INT,
            rating DECIMAL(2,1),
            rating_time DATETIME,
            PRIMARY KEY (userId, movieId),
            FOREIGN KEY (movieId) REFERENCES movies(movieId)
);

CREATE TABLE IF NOT EXISTS links(
            movieId INT PRIMARY KEY,
            imdbId VARCHAR(20),
            tmdbId INT
);

-- 2. Actors/Actresses table
-- CREATE TABLE actors (
--     id INT PRIMARY KEY,       -- TMDB person ID
--     name VARCHAR(255) NOT NULL,
--     gender TINYINT,           -- 0=unknown, 1=female, 2=male
--     profile_path VARCHAR(255) -- relative path to profile image
-- );

-- 3. Characters table (links actors to movies)
-- CREATE TABLE characters (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     movie_id INT NOT NULL,
--     actor_id INT NOT NULL,
--     character_name VARCHAR(255),
--     cast_order INT,           -- credit order
--     credit_id VARCHAR(255),   -- optional TMDB credit ID
--     FOREIGN KEY (movie_id) REFERENCES movies(id),
--     FOREIGN KEY (actor_id) REFERENCES actors(id)
-- );

