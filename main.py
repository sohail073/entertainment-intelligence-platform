from tmdb_etl.tmdb_extract import fetch_genres, fetch_tmdb_data, save_raw_json
from tmdb_etl.tmdb_transform import read_raw_json_files, parse_movie_data
from tmdb_etl.tmdb_load import load_dim_genres, load_dim_movies, load_movie_genres, load_fact_movie_metrics, load_dim_dates

def run_etl():

    print("Fetching and loading genres...")
    genres_data = fetch_genres()
    if genres_data:
        load_dim_genres(genres_data)
 
    tasks = [
        ("trending/movie/day", "trending_day"),
        ("trending/movie/week", "trending_week"),
        ("movie/top_rated", "top_rated"),
        ("movie/popular", "popular")
    ]
    
    for endpoint, filename in tasks:
        data = fetch_tmdb_data(endpoint)
        save_raw_json(data, filename)
    

    for data, date_id, feed_id in read_raw_json_files():
        parsed = parse_movie_data(data, feed_id, date_id)
        
        if parsed:
            load_dim_dates(date_id)
            load_dim_movies(parsed["dim_movies"])
            load_movie_genres(parsed["movie_genres"])  
            load_fact_movie_metrics(parsed["fact_movie_metrics"])

if __name__ == "__main__":
    run_etl()