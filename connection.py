import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print("Database connection established.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
    
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        conn.close()
        print("Database connection closed.")