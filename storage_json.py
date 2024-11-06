import json
from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        """Load database"""
        with open(self.file_path, "r") as fileobj:
            return json.load(fileobj)

    def save(self, data):
        """Save database"""
        with open(self.file_path, "w") as fileobj:
            json.dump(data, fileobj, indent=4)

    def list_movies(self):
        """Return the list of movies"""
        return self.load()

    def add_movie(self, title, year, rating, poster_url, imdb_id):
        """Add a movie to the database"""
        movies = self.load()
        movies[title] = {
            "title": title,
            "year": year,
            "rating": rating,
            "poster_url": poster_url,
            "imdb_id": imdb_id,
        }
        self.save(movies)

    def delete_movie(self, title):
        """Delete a movie from the database"""
        movies = self.load()
        if title in movies:
            del movies[title]
            self.save(movies)

    def update_movie(self, title, note):
        """Update movie notes"""
        movies = self.load()
        if title in movies:
            movies[title]['note'] = note
            self.save(movies)
