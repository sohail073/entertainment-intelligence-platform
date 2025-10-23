import os
import json
from dotenv import load_dotenv 

load_dotenv()

def read_raw_json_files():
    raw_data_dir = os.getenv("RAW_DATA_DIR")
    
    print(raw_data_dir)

    json_files = [f for f in os.listdir(raw_data_dir) if f.endswith(".json")]

    if not json_files:
        print("No JSON files found in the raw data directory.")
        return

    for file_name in json_files:
        file_path = os.path.join(raw_data_dir, file_name)
        print(f"\nReading file: {file_name}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            parse_json_files(data)
            print(f"Successfully parsed")
            
def parse_json_files(data):
    
    # print(data)
    
    if "results" in data:
        for item in data["results"][:5]:  
            title = item.get("title", "N/A")
            release_date = item.get("release_date", "N/A")
            print(f"Title: {title}, Release Date: {release_date}")
    else:
        print("No 'results' key found in the JSON data.")
    
if __name__ == "__main__":
    read_raw_json_files()
