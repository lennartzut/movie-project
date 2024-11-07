import argparse
import os
from movie_app import MovieApp, StorageCsv, StorageJson


def main():
    """Main function to initialize and run the movie app."""
    parser = argparse.ArgumentParser(
        description="Start the Movie App with a specified storage "
                    "file.")
    parser.add_argument("storage_file",
                        help="The storage file (JSON or CSV) to be "
                             "used for storing movie data.")

    args = parser.parse_args()
    storage_file = os.path.join("data", args.storage_file)

    _, file_extension = os.path.splitext(storage_file)

    if file_extension == ".json":
        storage = StorageJson(storage_file)
    elif file_extension == ".csv":
        storage = StorageCsv(storage_file)
    else:
        print(
            "Error: Unsupported file type. Please use a .json or "
            ".csv file.")
        return

    app = MovieApp(storage)
    app.run()


if __name__ == "__main__":
    main()
