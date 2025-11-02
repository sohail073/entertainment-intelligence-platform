from connection import get_db_connection
from datetime import datetime, timedelta

conn = get_db_connection()
cursor = conn.cursor()

def load_dim_dates(date_id):
    check_query = "SELECT 1 FROM dim_dates WHERE date_id = %s;"
    cursor.execute(check_query, (date_id,))
    
    if cursor.fetchone() is None:
        full_date = datetime.strptime(str(date_id), "%Y%m%d").date()
        insert_query = """
        INSERT INTO dim_dates (date_id, full_date, year, month, day, week)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            date_id,
            full_date,
            full_date.year,
            full_date.month,
            full_date.day,
            full_date.isocalendar()[1]
        ))
        conn.commit()
        print(f"Inserted {date_id} into dim_dates.")

def load_dim_genres(genres_data):
    """Load genre dimension data (one-time setup)"""
    if not genres_data or "genres" not in genres_data:
        print("No genre data to load")
        return
    
    insert_query = """
    INSERT INTO dim_genres (genre_id, genre_name)
    VALUES (%s, %s)
    ON CONFLICT (genre_id) DO UPDATE 
    SET genre_name = EXCLUDED.genre_name;
    """
    
    for genre in genres_data["genres"]:
        cursor.execute(insert_query, (
            genre["id"],
            genre["name"]
        ))
    
    conn.commit()
    print(f"Loaded {len(genres_data['genres'])} genres into dim_genres.")

def load_dim_movies(dim_movies):
    insert_query = """
    INSERT INTO dim_movies (movie_id, title, overview, release_date, original_language, poster_path, backdrop_path)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (movie_id) DO NOTHING;
    """
    for movie in dim_movies:
        cursor.execute(insert_query, (
            movie["movie_id"],
            movie["title"],
            movie["overview"],
            movie["release_date"],
            movie["original_language"],
            movie["poster_path"],
            movie["backdrop_path"]
        ))
    conn.commit()
    print(f"Inserted {len(dim_movies)} records into dim_movies.")
    
def load_movie_genres(movie_genres):
    insert_query = """
    INSERT INTO movie_genres (movie_id, genre_id)
    VALUES (%s, %s)
    ON CONFLICT DO NOTHING;
    """
    for mg in movie_genres:
        cursor.execute(insert_query, (
            mg["movie_id"],
            mg["genre_id"]
        ))
    conn.commit()
    print(f"Inserted {len(movie_genres)} records into movie_genres.")
    
def load_fact_movie_metrics(fact_movie_metrics):
    insert_query = """
    INSERT INTO fact_movie_metrics (movie_id, feed_id, date_id, popularity, vote_average, vote_count, rank_position, fetch_timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    for fm in fact_movie_metrics:
        cursor.execute(insert_query, (
            fm["movie_id"],
            fm["feed_id"],
            fm["date_id"],
            fm["popularity"],
            fm["vote_average"],
            fm["vote_count"],
            fm["rank_position"],
            fm["fetch_timestamp"]
        ))
    conn.commit()
    print(f"Inserted {len(fact_movie_metrics)} records into fact_metrics.")
    
