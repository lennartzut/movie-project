import json


DATABASE = "data.json"


def load_json_file():
    """Load database"""
    with open(DATABASE, "r") as fileobj:
        return json.load(fileobj)


def save_json_file(movie_db):
    """Save database"""
    with open(DATABASE, "w") as fileobj:
        json.dump(movie_db, fileobj, indent=4)


def list_movies():
    """Return the list of movies"""
    return load_json_file()


def add_movie(title, year, rating):
    """Add a movie to the database"""
    movies = load_json_file()
    movies[title] = {
                    "title": title,
                    "year": year,
                    "rating": rating
                    }
    save_json_file(movies)


def delete_movie(title):
    """Delete a movie from the database"""
    movies = load_json_file()
    if title in movies:
        del movies[title]
        save_json_file(movies)


def update_movie(title, rating):
    """Update the rating of a movie."""
    movies = load_json_file()
    if title in movies:
        movies[title]['rating'] = rating
        save_json_file(movies)
