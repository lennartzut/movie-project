from movie_app import MovieApp
from storage_json import StorageJson


def main():
    """Main function to initialize and run the movie app."""
    storage = StorageJson("data.json")

    app = MovieApp(storage)

    app.run()


if __name__ == "__main__":
    main()
