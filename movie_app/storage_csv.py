import csv
from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        """Load database from CSV"""
        movies = {}
        with open(self.file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                movies[row['title']] = {
                    "title": row['title'],
                    "year": int(row['year']),
                    "rating": float(row['rating']),
                    "poster_url": row['poster_url'],
                    "imdb_id": row['imdb_id'],
                    "note": row.get('note', '')
                }
        return movies

    def save(self, data):
        """Save database to CSV"""
        with open(self.file_name, "w", newline='') as csvfile:
            fieldnames = ["title", "year", "rating", "poster_url",
                          "imdb_id", "note"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for movie in data.values():
                writer.writerow(movie)

    def list_movies(self):
        """Return the list of movies"""
        return self.load()

    def add_movie(self, title, year, rating, poster_url, imdb_id):
        """Add a movie to the CSV database"""
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
        """Delete a movie from the CSV database"""
        movies = self.load()
        if title in movies:
            del movies[title]
            self.save(movies)

    def update_movie(self, title, note):
        """Update movie notes in the CSV database"""
        movies = self.load()
        if title in movies:
            movies[title]['note'] = note
            self.save(movies)
