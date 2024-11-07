import json
import os
import unittest
from movie_app import StorageJson


class TestStorageJson(unittest.TestCase):
    def setUp(self):
        """Create temporary JSON file for testing."""
        self.json_file = "test_movies.json"
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as file:
                json.dump({}, file)  # Create an empty JSON object

        self.storage = StorageJson(self.json_file)

    def tearDown(self):
        """Remove temporary file after each test."""
        if os.path.exists(self.json_file):
            os.remove(self.json_file)

    def test_add_movie(self):
        """Test adding a movie to JSON storage"""
        self.storage.add_movie("Inception",
                               2010,
                               8.8,
                               "http://example.com/poster",
                               "tt1375666")
        movies = self.storage.list_movies()
        self.assertIn("Inception", movies)

    def test_delete_movie(self):
        """Test deleting a movie from JSON storage"""
        self.storage.add_movie("Inception",
                               2010,
                               8.8,
                               "http://example.com/poster",
                               "tt1375666")
        self.storage.delete_movie("Inception")
        movies = self.storage.list_movies()
        self.assertNotIn("Inception", movies)

    def test_update_movie_notes(self):
        """Test updating movie notes in JSON storage"""
        self.storage.add_movie("Inception",
                               2010,
                               8.8,
                               "http://example.com/poster",
                               "tt1375666")
        self.storage.update_movie("Inception", "Great movie!")
        movies = self.storage.list_movies()
        self.assertEqual(movies["Inception"]["note"], "Great movie!")


if __name__ == "__main__":
    unittest.main()
