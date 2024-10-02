import movie_storage


def get_minimal_rating():
    """Prompt the user to enter a minimal rating"""
    while True:
        user_input = input("\nEnter minimum rating (leave blank for "
                           "no minimum rating): ").strip()
        if not user_input:
            return None
        try:
            rating = float(user_input)
            if 0 <= rating <= 10:
                return rating
            print("\nPlease enter a rating between 0 and 10.")
        except ValueError:
            print("\nInvalid input. Please enter a valid rating.")


def get_start_year():
    """Prompt the user to enter a start year"""
    while True:
        user_input = input("\nEnter start year (leave blank for no "
                           "start year): ").strip()
        if not user_input:
            return None
        try:
            year = int(user_input)
            if year > 0:
                return year
            print("\nPlease enter a valid positive year.")
        except ValueError:
            print("\nInvalid input. Please enter a valid year.")


def get_end_year():
    """Prompt the user to enter an end year"""
    while True:
        user_input = input("\nEnter end year (leave blank for no "
                           "end year): ").strip()
        if not user_input:
            return None
        try:
            year = int(user_input)
            if year > 0:
                return year
            print("\nPlease enter a valid positive year.")
        except ValueError:
            print("\nInvalid input. Please enter a valid year.")


def filter_movie(movie_info, minimal_rating=None, start_year=None,
                 end_year=None):
    """Check if a movie meets the filtering criteria"""
    rating = movie_info.get("rating")
    year = movie_info.get("year")
    if minimal_rating is not None and rating < minimal_rating:
        return False
    if start_year is not None and year < start_year:
        return False
    if end_year is not None and year > end_year:
        return False
    return True


def show_filtered_movies_with_input():
    """
    Filter and display movies based on user input for
    rating and year range
    """
    movies = movie_storage.load_json_file()
    minimal_rating = get_minimal_rating()
    start_year = get_start_year()
    end_year = get_end_year()
    filtered_movies = {
        title: info for title, info in movies.items()
        if filter_movie(info, minimal_rating, start_year, end_year)
    }
    if not filtered_movies:
        print("\nNo movies found matching the criteria.")
    else:
        for title, info in filtered_movies.items():
            year = info.get("year")
            rating = info.get("rating")
            print(f'{title} ({year}): {rating:.1f}')
