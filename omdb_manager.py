import requests
import os
from dotenv import  load_dotenv
load_dotenv()

BASE_URL = "http://www.omdbapi.com/"

def fetch_movie_data(title: str) -> dict | None:
    params = {
        "apikey": os.getenv("API_KEY"),
        "t": title
    }
    response = requests.get(BASE_URL, params=params, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("Response") == "False":
        return None

    return {
        "title": data.get("Title", "N/A"),
        "year": data.get("Year", "N/A"),
        "rating": data.get("imdbRating", "N/A"),
        "director": data.get("Director", "N/A"),
        "poster": data.get("Poster", "")
    }
if __name__ == "__main__":
    movie = fetch_movie_data("The Matrix")
    if movie:
        for key, value in movie.items():
            print(f"{key.capitalize()}: {value}")

    else:
        print("No movie found")
