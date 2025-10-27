import requests 
import json 
import os 
from datetime import datetime
from dotenv import load_dotenv 

load_dotenv() 

# Your TMDB API token 
ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN") 

def fetch_genres():
    """Fetch all movie genres from TMDB"""
    url = "https://api.themoviedb.org/3/genre/movie/list"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching genres: {response.status_code}")
        return None

# Function to fetch data from a given endpoint 
def fetch_tmdb_data(endpoint: str): 
    url = f"https://api.themoviedb.org/3/{endpoint}" 
    
    headers = { 
               "Authorization": f"Bearer {ACCESS_TOKEN}", "accept": "application/json" 
               } 
    
    response = requests.get(url, headers=headers) 
    
    if response.status_code == 200: 
        return response.json() 
    else: 
        print(f"Error {response.status_code}: {response.text}") 
        return None

def save_raw_json(data, filename):
    
    base_dir = os.getenv("RAW_DATA_DIR")
    os.makedirs(base_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d")
    filepath = os.path.join(base_dir, f"{filename}_{timestamp}.json")
    
    # Save JSON data
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved")
    

if __name__ == "__main__":
    
    tasks = [
        ("trending/movie/day", "trending_day"),
        ("trending/movie/week", "trending_week"),
        ("movie/top_rated", "top_rated"),
        ("movie/popular", "popular")
    ]
    
    for endpoint, filename in tasks:
        data = fetch_tmdb_data(endpoint)
        print('=' * 20)
        print(f'Completed for {filename.replace("_", " ").title()}\n')
        print('=' * 20)
        save_raw_json(data, filename)


