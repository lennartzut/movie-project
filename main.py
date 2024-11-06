from movie_app import MovieApp, StorageCsv, StorageJson


def main():
    """Main function to initialize and run the movie app."""
    storage = StorageCsv('data/movies.csv')
    app = MovieApp(storage)
    app.run()


if __name__ == "__main__":
    main()
