-- Movie Dim Table
CREATE TABLE dim_movies (
	movie_id INT PRIMARY KEY,
	title VARCHAR(255),
	overview TEXT,
    release_date DATE,
    original_language VARCHAR(10),
    poster_path TEXT,
    backdrop_path TEXT
);

-- Genre Dim Table
CREATE TABLE dim_genres (
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(100)
);

-- Source Type Dim Table (trending_day, week, top_rated, popular)
CREATE TABLE dim_source_types (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(50) UNIQUE
);

-- Date Dim Table
CREATE TABLE dim_dates (
    date_id SERIAL PRIMARY KEY,
    full_date DATE UNIQUE,
    year INT,
    month INT,
    day INT,
    week INT
);

-- Fact Movie Metrics Table
CREATE TABLE fact_movie_metrics (
    fact_id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES dim_movies(movie_id),
    source_id INT REFERENCES dim_source_types(source_id),
    date_id INT REFERENCES dim_dates(date_id),
    popularity FLOAT,
    vote_average FLOAT,
    vote_count INT,
    rank_position INT,
    fetch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fact Reddit Sentiment Table
CREATE TABLE fact_reddit_sentiment (
    reddit_fact_id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES dim_movies(movie_id),
	post_url VARCHAR(500) UNIQUE,
    subreddit VARCHAR(100),
    post_title TEXT,
    sentiment_score FLOAT,
    sentiment_label VARCHAR(20),
    summary TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- create table bridge 
CREATE TABLE movie_genres (
    movie_id INT REFERENCES dim_movies(movie_id),
    genre_id INT REFERENCES dim_genres(genre_id),
    PRIMARY KEY (movie_id, genre_id)
);
