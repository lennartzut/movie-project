import csv
import json
import os
import unittest
from movie_app import MovieApp, StorageCsv, StorageJson


class TestMovieApp(unittest.TestCase):
    def setUp(self):
        """Create temporary JSON and CSV files for testing."""
        self.json_file = "test_movies.json"
        self.csv_file = "test_movies.csv"

        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as file:
                json.dump({}, file)

        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file,
                                        fieldnames=["title", "year",
                                                    "rating",
                                                    "poster_url",
                                                    "imdb_id",
                                                    "note"])
                writer.writeheader()
        self.json_storage = StorageJson(self.json_file)
        self.csv_storage = StorageCsv(self.csv_file)
        self.json_app = MovieApp(self.json_storage)
        self.csv_app = MovieApp(self.csv_storage)

    def tearDown(self):
        """Remove temporary files after each test."""
        if os.path.exists(self.json_file):
            os.remove(self.json_file)
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_list_movies_json(self):
        """Test listing movies from JSON storage in the MovieApp"""
        self.json_storage.add_movie("Inception", 2010, 8.8,
                                    "http://example.com/poster",
                                    "tt1375666")
        movies = self.json_app._storage.list_movies()
        self.assertEqual(len(movies), 1)

    def test_list_movies_csv(self):
        """Test listing movies from CSV storage in the MovieApp"""
        self.csv_storage.add_movie("The Matrix", 1999, 8.7,
                                   "http://example.com/poster",
                                   "tt0133093")
        movies = self.csv_app._storage.list_movies()
        self.assertEqual(len(movies), 1)


if __name__ == "__main__":
    unittest.main()
