import movie_filter
import movie_lookup
import movie_stats
import movie_storage
from api import make_api_request
import os


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
        "10. Filter movies",
        "11. Generate website"
    ]
    print("\nMenu:")
    for option in menu_options:
        print(option)


def get_add_movie_info():
    """Prompt the user to enter movie title to add"""
    while True:
        title = input("\nEnter new movie name: ").strip()
        if not title:
            print("\nInput cannot be empty, please try again.")
            continue
        formatted_title = format_title(title)
        if formatted_title in movie_storage.list_movies():
            print(f"\nMovie {formatted_title} already exist!")
            return None, None, None, None
        movie_data = make_api_request(formatted_title)
        if movie_data and movie_data.get("Response") == "True":
            movie_title = movie_data.get("Title")
            year = movie_data.get("Year")
            rating = movie_data.get("imdbRating")
            poster_url = movie_data.get("Poster")
            if year != "N/A":
                year = int(year)
            else:
                year = 0
            if rating != "N/A":
                rating = float(rating)
            else:
                rating = 0.0
            return movie_title, year, rating, poster_url
        else:
            print("\nCould not find the movie in the OMDb "
                  "database, please try again.")


def get_update_movie_info():
    """Prompt the user to enter movie title and add notes"""
    title = input("\nEnter movie name: ").strip()
    formatted_title = format_title(title)
    if formatted_title in movie_storage.list_movies():
        note = input("\nEnter movie notes: ").strip()
        return formatted_title, note
    print(f"\nMovie \"{title}\" doesn't exist!")
    return None, None


def get_delete_movie_info():
    """Prompt the user to enter movie title to delete"""
    while True:
        title = input("\nEnter movie name to delete: ").strip()
        if not title:
            print("\nInput cannot be empty, please try again.")
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
    """Add a new movie using the OMDb API"""
    title, year, rating, poster_url = get_add_movie_info()
    if title:
        movie_storage.add_movie(title, year, rating, poster_url)
        print(f"\nMovie '{title}' successfully added.")


def delete_movie():
    """Delete a movie"""
    title = get_delete_movie_info()
    if title:
        movie_storage.delete_movie(title)
        print(f"\nMovie '{title}' successfully deleted.")


def update_movie():
    """Update a movie's notes"""
    title, note = get_update_movie_info()
    if title:
        movie_storage.update_movie_notes(title, note)
        print(f"\nMovie '{title}' successfully updated.")


def generate_website():
    """Generate the website from the movie database"""
    movies = movie_storage.list_movies()
    if not movies:
        print("\nNo movies to display on the website.")
        return

    with open(os.path.join("_static", "index_template.html"),
              "r") as template_file:
        template_content = template_file.read()

    movie_grid = ""
    for movie_info in movies.values():
        note = movie_info.get('note', '')
        movie_grid += f'''
        <li>
            <div class="movie">
                <img class="movie-poster" src="{movie_info.get('poster_url')}" alt="{movie_info.get('title')} poster" title="{note}">
                <div class="movie-title">{movie_info.get('title')}</div>
                <div class="movie-year">{movie_info.get('year')}</div>
                <div class="movie-rating">Rating: {movie_info.get('rating'):.1f}</div>
            </div>
        </li>
        '''

    updated_content = template_content.replace("__TEMPLATE_TITLE__",
                                               "My Movie Collection")
    updated_content = updated_content.replace(
        "__TEMPLATE_MOVIE_GRID__", movie_grid)

    with open(os.path.join("_static", "index.html"),
              "w") as output_file:
        output_file.write(updated_content)

    print("Website was generated successfully.")


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
        11: generate_website,
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
        print(input("\nPress enter to continue."))


if __name__ == "__main__":
    main()
