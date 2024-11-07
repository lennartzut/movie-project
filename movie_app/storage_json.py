import json
from movie_app.istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        """Load database from JSON"""
        try:
            with open(self.file_path, "r") as fileobj:
                movies = json.load(fileobj)
        except json.JSONDecodeError:
            self.save({})
            return {}
        return movies

    def save(self, data):
        """Save database to JSON"""
        with open(self.file_path, "w") as fileobj:
            json.dump(data, fileobj, indent=4)

    def list_movies(self):
        """Return the list of movies"""
        return self.load()

    def add_movie(self, title, year, rating, poster_url, imdb_id):
        """Add a movie to the JSON database"""
        movies = self.load()
        movies[title] = {
            "title": title,
            "year": year,
            "rating": rating,
            "poster_url": poster_url,
            "imdb_id": imdb_id,
            "note": ""
        }
        self.save(movies)

    def delete_movie(self, title):
        """Delete a movie from the JSON database"""
        movies = self.load()
        if title in movies:
            del movies[title]
            self.save(movies)

    def update_movie(self, title, note):
        """Update movie notes in the JSON database"""
        movies = self.load()
        if title in movies:
            movies[title]['note'] = note
            self.save(movies)
