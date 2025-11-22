SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS movies_metadata;
DROP TABLE IF EXISTS movie_languages;
DROP TABLE IF EXISTS spoken_languages;
DROP TABLE IF EXISTS movie_countries;
DROP TABLE IF EXISTS production_countries;
DROP TABLE IF EXISTS movie_companies;
DROP TABLE IF EXISTS production_companies;
DROP TABLE IF EXISTS movie_keywords;
DROP TABLE IF EXISTS keywords;
DROP TABLE IF EXISTS crew_members;
DROP TABLE IF EXISTS cast_members;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS movie_genres;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS movies;
SET FOREIGN_KEY_CHECKS = 1;

-- Movies table
CREATE TABLE IF NOT EXISTS movies (
    id INT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    original_title VARCHAR(500),
    overview TEXT,
    release_date DATE,
    runtime FLOAT,
    budget BIGINT,
    revenue BIGINT,
    popularity FLOAT,
    vote_average FLOAT,
    vote_count INT,
    status VARCHAR(50),
    tagline VARCHAR(500)
);

-- Genres table
CREATE TABLE IF NOT EXISTS genres (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Movie Genres link table
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);

-- People table (Actors, Directors, Crew)
CREATE TABLE IF NOT EXISTS people (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    gender INT, -- 0=Unknown, 1=Female, 2=Male
    profile_path VARCHAR(255)
);

-- Cast table
CREATE TABLE IF NOT EXISTS cast_members (
    credit_id VARCHAR(255) PRIMARY KEY,
    movie_id INT,
    person_id INT,
    character_name VARCHAR(500),
    order_index INT,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (person_id) REFERENCES people(id)
);

-- Crew table
CREATE TABLE IF NOT EXISTS crew_members (
    credit_id VARCHAR(255) PRIMARY KEY,
    movie_id INT,
    person_id INT,
    job VARCHAR(255),
    department VARCHAR(255),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (person_id) REFERENCES people(id)
);

-- Keywords table
CREATE TABLE IF NOT EXISTS keywords (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Movie Keywords link table
CREATE TABLE IF NOT EXISTS movie_keywords (
    movie_id INT,
    keyword_id INT,
    PRIMARY KEY (movie_id, keyword_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Production Companies table
CREATE TABLE IF NOT EXISTS production_companies (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Movie Companies link table
CREATE TABLE IF NOT EXISTS movie_companies (
    movie_id INT,
    company_id INT,
    PRIMARY KEY (movie_id, company_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (company_id) REFERENCES production_companies(id)
);

-- Production Countries table
CREATE TABLE IF NOT EXISTS production_countries (
    iso_3166_1 VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Movie Countries link table
CREATE TABLE IF NOT EXISTS movie_countries (
    movie_id INT,
    country_code VARCHAR(10),
    PRIMARY KEY (movie_id, country_code),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (country_code) REFERENCES production_countries(iso_3166_1)
);

-- Spoken Languages table
CREATE TABLE IF NOT EXISTS spoken_languages (
    iso_639_1 VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Movie Languages link table
CREATE TABLE IF NOT EXISTS movie_languages (
    movie_id INT,
    language_code VARCHAR(10),
    PRIMARY KEY (movie_id, language_code),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (language_code) REFERENCES spoken_languages(iso_639_1)
);

CREATE TABLE IF NOT EXISTS movie_posters (
    movie_id INT PRIMARY KEY,
    image LONGBLOB,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    rating FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

