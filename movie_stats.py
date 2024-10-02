import movie_storage


def show_stats():
    """Print statistics about the movies in the database"""
    sorted_movies = sort_movies_by_rating()
    if not sorted_movies:
        print("\nNo movies in the database to show stats.")
        return
    average = calc_average_rating()
    median = get_median_rating(sorted_movies)
    sorted_list = list(sorted_movies.items())
    best_movie_title, best_movie_info = sorted_list[0]
    worst_movie_title, worst_movie_info = sorted_list[-1]
    print(f"\nAverage rating: {average:.1f}")
    print(f"Median rating: {median:.1f}")
    print(f"Best movie: {best_movie_title}, "
          f"{best_movie_info.get('rating')}")
    print(f"Worst movie: {worst_movie_title}, "
          f"{worst_movie_info.get('rating')}")


def calc_average_rating():
    """Calculate and return the average rating"""
    movies = movie_storage.load_json_file()
    if not movies:
        return 0
    total_ratings = sum(movie["rating"] for movie in movies.values())
    return total_ratings / len(movies)


def get_median_rating(sorted_movies):
    """Get and return the median of the ratings"""
    ratings = [movie_info["rating"] for movie_info in
               sorted_movies.values()]
    if not ratings:
        return 0
    ratings.sort()
    middle = len(ratings) // 2
    if len(ratings) % 2 == 0:
        return (ratings[middle - 1] + ratings[middle]) / 2
    return ratings[middle]


def print_sorted_movies_by_rating():
    """Print the sorted movies by rating"""
    sorted_movies = sort_movies_by_rating()
    if not sorted_movies:
        print("\nNo movies in the database to sort by rating.")
        return
    for movie_title, movie_info in sorted_movies.items():
        print(f'{movie_title}: {movie_info["rating"]:.1f}')


def sort_movies_by_rating():
    """Return a sorted dictionary of movies by rating"""
    movies = movie_storage.load_json_file()
    return dict(sorted(movies.items(), key=lambda
                item: item[1].get("rating"), reverse=True)
                )


def get_sort_order():
    """
    Prompt the user for sort order and return True if latest first,
    else False
    """
    while True:
        choice = input("\nDo you want the latest movie first?"
                       " (Y/N): ").strip().lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        print("\nPlease enter 'Y' or 'N'.")


def sort_movies_by_year():
    """Sort the movies by year and print them"""
    movies = movie_storage.load_json_file()
    if not movies:
        print("\nNo movies in the database to sort by year.")
        return
    latest_first = get_sort_order()
    sorted_movies = dict(sorted(movies.items(),
                                key=lambda item:
                                item[1].get("year", 0),
                                reverse=latest_first
                                )
                         )
    for movie_title, movie_info in sorted_movies.items():
        print(f'{movie_title} ({movie_info.get("year")}):'
              f' {movie_info.get("rating"):.1f}')
