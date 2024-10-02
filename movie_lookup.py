import random
import movie_storage


def random_movie():
    """Print a random movie and its rating"""
    movies = movie_storage.load_json_file()
    if not movies:
        print("\nNo movies in the database to pick a random movie.")
        return
    movie_title, movie_info = random.choice(list(movies.items()))
    print(f'\nYour movie for tonight: {movie_title}, it\'s rated '
          f'{movie_info["rating"]:.1f}')


def search_movie():
    """
    Ask the user to enter a part of a movie name and search
    the database
    """
    movies = movie_storage.load_json_file()
    if not movies:
        print("\nNo movies in the database to search.")
        return
    while True:
        part_of_title = input("\nEnter part of movie name: ").strip()
        if not part_of_title:
            print("\nInput cannot be empty, please try again.")
            continue
        matches = [movie for movie in movies if
                   part_of_title.casefold() in movie.casefold()]
        if matches:
            print("\nMovies found:")
            for match in matches:
                print(match)
            break
        print(f"\n\"{part_of_title}\" not found in database, "
              f"please try again.")
