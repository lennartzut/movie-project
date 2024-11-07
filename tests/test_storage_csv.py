import csv
import os
import unittest
from movie_app import StorageCsv


class TestStorageCsv(unittest.TestCase):
    def setUp(self):
        """Create temporary CSV file for testing."""
        self.csv_file = "test_movies.csv"
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["title",
                                                          "year",
                                                          "rating",
                                                          "poster_url",
                                                          "imdb_id",
                                                          "note"])
                writer.writeheader()

        self.storage = StorageCsv(self.csv_file)

    def tearDown(self):
        """Remove temporary file after each test."""
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_add_movie(self):
        """Test adding a movie to CSV storage"""
        self.storage.add_movie("Inception",
                               2010,
                               8.8,
                               "http://example.com/poster",
                               "tt1375666")
        movies = self.storage.list_movies()
        self.assertIn("Inception", movies)

    def test_delete_movie(self):
        """Test deleting a movie from CSV storage"""
        self.storage.add_movie("Inception",
                               2010,
                               8.8,
                               "http://example.com/poster",
                               "tt1375666")
        self.storage.delete_movie("Inception")
        movies = self.storage.list_movies()
        self.assertNotIn("Inception", movies)

    def test_update_movie_notes(self):
        """Test updating movie notes in CSV storage"""
        self.storage.add_movie("Inception",
                               2010,
                               8.8,
                               "http://example.com/poster",
                               "tt1375666")
        self.storage.update_movie("Inception", "Must-watch movie!")
        movies = self.storage.list_movies()
        self.assertEqual(movies["Inception"]["note"],
                         "Must-watch movie!")


if __name__ == "__main__":
    unittest.main()
