import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')


def make_api_request(movie_title):
    """Make an API request to OMDB API with the provided
    movie title."""
    api_url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_title}"
    try:
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print("Error:", response.status_code, response.json())
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
