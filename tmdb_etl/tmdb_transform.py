import os
import json
from dotenv import load_dotenv 
from datetime import datetime

load_dotenv()

def read_raw_json_files():
    raw_data_dir = os.getenv("RAW_DATA_DIR")
    
    today_str = datetime.now().strftime("%Y%m%d")

    json_files = [f for f in os.listdir(raw_data_dir) if f.endswith(".json")]

    for file_name in json_files:
        if today_str in file_name:  
            file_path = os.path.join(raw_data_dir, file_name)
            print(f"\nReading file: {file_name}")

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                feed_map = {
                    "trending_day": 1,
                    "trending_week": 2,
                    "top_rated": 3,
                    "popular": 4
                }
                
                feed_name = "_".join(file_name.replace(".json", "").split("_")[:-1])
                
                yield data, today_str, feed_map.get(feed_name, 0)

def parse_movie_data(data, feed_id, date_id):
    dim_movies = []
    movie_genres = []
    fact_metrics = []

    if "results" not in data:
        print("No 'results' key found in the JSON data.")
        return None

    for item in data["results"]:

        movie = {
            "movie_id": item.get("id"),
            "title": item.get("title"),
            "overview": item.get("overview"),
            "release_date": item.get("release_date"),
            "original_language": item.get("original_language"),
            "poster_path": item.get("poster_path"),
            "backdrop_path": item.get("backdrop_path")
        }
        dim_movies.append(movie)

        for genre in item.get("genre_ids", []):
            movie_genres.append({
                "movie_id": item.get("id"),
                "genre_id": genre
            })

        for rank, item in enumerate(data["results"], start=1):
            fact_metrics.append({
                "movie_id": item.get("id"),
                "feed_id": feed_id,
                "date_id": date_id,
                "popularity": item.get("popularity"),
                "vote_average": item.get("vote_average"),
                "vote_count": item.get("vote_count"),
                "rank_position": rank,
                "fetch_timestamp": datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            })

    return {
        "dim_movies": dim_movies,
        "movie_genres": movie_genres,
        "fact_metrics": fact_metrics
    }    
    
if __name__ == "__main__":
    
    for data, date_id, feed_id in read_raw_json_files():
        parsed_data = parse_movie_data(data, feed_id, date_id)
        print(f"\nParsed data for feed: {feed_id}")
        
