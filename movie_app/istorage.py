from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def load(self):
        """Load and return the movie data."""
        pass

    @abstractmethod
    def save(self, data):
        """Save the movie data."""
        pass

    @abstractmethod
    def list_movies(self):
        """Return the list of movies."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster_url, imdb_id):
        """Add a movie to the database."""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Delete a movie from the database."""
        pass

    @abstractmethod
    def update_movie(self, title, note):
        """Update movie notes."""
        pass
