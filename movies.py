import movie_storage
import movie_stats
import movie_lookup
import movie_filter


def show_menu():
    """Display menu options"""
    menu_options = [
        "0. Exit",
        "1. List movies",
        "2. Add movie",
        "3. Delete movie",
        "4. Update movie",
        "5. Stats",
        "6. Random movie",
        "7. Search movie",
        "8. Movies sorted by rating",
        "9. Movies sorted by year",
        "10. Filter movies"
    ]
    print("\nMenu:")
    for option in menu_options:
        print(option)


def get_add_movie_info():
    """Prompt the user to enter movie info to add"""
    while True:
        title = input("\nEnter new movie name: ").strip()
        if not title:
            print("\nInput cannot be empty, please try again")
            continue
        formatted_title = format_title(title)
        if formatted_title in movie_storage.list_movies():
            print(f"\nMovie {formatted_title} already exist!")
            return None, None, None
        try:
            year = int(input("\nEnter new movie year: ").strip())
            rating = float(input("\nEnter new movie rating: "
                                 "").strip())
            if 0 < rating < 10:
                return formatted_title, year, rating
        except ValueError:
            print("\nInvalid input, please try again")


def get_update_movie_info():
    """Prompt the user to enter movie title and the update rating"""
    title = input("\nEnter movie name: ").strip()
    formatted_title = format_title(title)
    if formatted_title in movie_storage.list_movies():
        while True:
            rating = float(
                input("\nEnter new movie rating: ").strip())
            if 0 < rating < 10:
                return formatted_title, rating
            print("Invalid input, please try again")
    print(f"\nMovie \"{title}\" doesn't exist!")
    return None, None


def get_delete_movie_info():
    """Prompt the user to enter movie title to delete"""
    while True:
        title = input("\nEnter movie name to delete: ").strip()
        if not title:
            print("\nInput cannot be empty, please try again")
            continue
        formatted_title = format_title(title)
        if formatted_title in movie_storage.list_movies():
            return formatted_title
        print(f"\nMovie \"{title}\" doesn't exist!")
        return None


def format_title(title):
    """Format the input title to be consistent with the database"""
    words = title.split()
    formatted_words = []
    for word in words:
        if word.lower().endswith("'s"):
            formatted_word = word[:-2].capitalize() + "'s"
        else:
            formatted_word = word.capitalize()
        formatted_words.append(formatted_word)
    return " ".join(formatted_words)


def show_list_movies():
    """List all movies"""
    movies = movie_storage.list_movies()
    if movies:
        print(f"\n{len(movies)} movies in total")
        for movie_info in movies.values():
            print(f"{movie_info.get('title')} "
                  f"({movie_info.get('year')}): "
                  f"{movie_info.get('rating'):.1f}")
    else:
        print("\nNo movies in the database.")


def add_movie():
    """Add a new movie"""
    title, year, rating = get_add_movie_info()
    if title:
        movie_storage.add_movie(title, year, rating)
        print(f"\nMovie '{title}' successfully added.")


def delete_movie():
    """Delete a movie"""
    title = get_delete_movie_info()
    if title:
        movie_storage.delete_movie(title)
        print(f"\nMovie '{title}' successfully deleted.")


def update_movie():
    """Update a movie's rating"""
    title, rating = get_update_movie_info()
    if title:
        movie_storage.update_movie(title, rating)
        print(f"\nMovie '{title}' successfully updated.")


def exit_program():
    """Exit the program"""
    print("\nBye!")


def main():
    """Main function to run the program"""
    menu_functions = {
        0: exit_program,
        1: show_list_movies,
        2: add_movie,
        3: delete_movie,
        4: update_movie,
        5: movie_stats.show_stats,
        6: movie_lookup.random_movie,
        7: movie_lookup.search_movie,
        8: movie_stats.print_sorted_movies_by_rating,
        9: movie_stats.sort_movies_by_year,
        10: movie_filter.show_filtered_movies_with_input,
    }

    print("********** My Movies Database **********")
    while True:
        show_menu()
        try:
            choice = int(input("\nEnter choice (0-10): ").strip())
            if choice in menu_functions:
                try:
                    menu_functions[choice]()
                    if choice == 0:
                        break
                except (TypeError, KeyError):
                    continue
            else:
                print("\nInvalid choice, please try again.")
        except ValueError:
            print("\nInvalid input.")
        print(input("\nPress enter to continue "))


if __name__ == "__main__":
    main()
