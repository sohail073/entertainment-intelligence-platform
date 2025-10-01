import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Your TMDB API token
ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

# Function to fetch data from a given endpoint
def fetch_tmdb_data(endpoint: str):
    url = f"https://api.themoviedb.org/3/{endpoint}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


# Example calls:
if __name__ == "__main__":
    # Get trending movies this week
    # trending_movies = fetch_tmdb_data("trending/movie/week")
    # print(json.dumps(trending_movies, indent=2, ensure_ascii=False))

    # # Get popular TV shows
    # popular_tv = fetch_tmdb_data("tv/popular")
    # print('Popular TV Shows:\n')
    # print(json.dumps(popular_tv, indent=2, ensure_ascii=False))
    
    # popular_tv = fetch_tmdb_data("movie/top_rated")
    # print('Popular TV Shows:\n')
    # print(json.dumps(popular_tv, indent=2, ensure_ascii=False))
    
    popular_tv = fetch_tmdb_data("movie/popular")
    print('Popular TV Shows:\n')
    print(json.dumps(popular_tv, indent=2, ensure_ascii=False))
    
    