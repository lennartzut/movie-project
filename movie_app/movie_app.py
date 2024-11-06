import os
from api import make_api_request


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        movies = self._storage.list_movies()
        if movies:
            print(f"\n{len(movies)} movies in total")
            for movie_info in movies.values():
                print(f"{movie_info.get('title')} ("
                      f"{movie_info.get('year')}):"
                      f" {movie_info.get('rating'):.1f}")
        else:
            print("\nNo movies in the database.")

    def _command_add_movie(self):
        title, year, rating, poster_url, imdb_id = (
            self.get_add_movie_info())
        if title:
            self._storage.add_movie(title, year, rating,
                                    poster_url, imdb_id)
            print(f"\nMovie '{title}' successfully added.")

    def _command_delete_movie(self):
        title = self.get_delete_movie_info()
        if title:
            self._storage.delete_movie(title)
            print(f"\nMovie '{title}' successfully deleted.")

    def _command_update_movie(self):
        title, note = self.get_update_movie_info()
        if title:
            self._storage.update_movie(title, note)
            print(f"\nMovie '{title}' successfully updated.")

    def _command_movie_stats(self):
        sorted_movies = self.sort_movies_by_rating()
        valid_movies = {k: v for k, v in sorted_movies.items() if
                        v.get("rating") > 0}
        if not valid_movies:
            print("\nNo movies in the database to show stats.")
            return
        average = self.calc_average_rating(valid_movies)
        median = self.get_median_rating(valid_movies)
        sorted_list = list(valid_movies.items())
        best_movie_title, best_movie_info = sorted_list[0]
        worst_movie_title, worst_movie_info = sorted_list[-1]
        print(f"\nAverage rating: {average:.1f}")
        print(f"Median rating: {median:.1f}")
        print(f"Best movie: {best_movie_title}, "
              f"{best_movie_info.get('rating')}")
        print(f"Worst movie: {worst_movie_title}, "
              f"{worst_movie_info.get('rating')}")

    def _command_random_movie(self):
        movies = self._storage.list_movies()
        valid_movies = {k: v for k, v in movies.items() if v.get(
            "rating") > 0}
        if not valid_movies:
            print("\nNo movies in the database to pick a random "
                  "movie.")
            return
        import random
        movie_title, movie_info = random.choice(list(
            valid_movies.items()))
        print(f"\nYour movie for tonight: {movie_title}, "
              f"it's rated {movie_info['rating']:.1f}")

    def _command_search_movie(self):
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies in the database to search.")
            return
        while True:
            part_of_title = input("\nEnter part of movie name: "
                                  "").strip()
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

    def _command_sort_movies_by_rating(self):
        sorted_movies = self.sort_movies_by_rating()
        if not sorted_movies:
            print("\nNo movies in the database to sort by rating.")
            return
        for movie_title, movie_info in sorted_movies.items():
            print(f"{movie_title}: {movie_info['rating']:.1f}")

    def _command_sort_movies_by_year(self):
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies in the database to sort by year.")
            return
        latest_first = self.get_sort_order()
        sorted_movies = dict(sorted(movies.items(), key=lambda
            item: item[1].get("year", 0), reverse=latest_first))
        for movie_title, movie_info in sorted_movies.items():
            print(f"{movie_title} ({movie_info.get('year')}): "
                  f"{movie_info.get('rating'):.1f}")

    def _command_filter_movies(self):
        movies = self._storage.list_movies()
        minimal_rating = self.get_minimal_rating()
        start_year = self.get_start_year()
        end_year = self.get_end_year()
        filtered_movies = {
            title: info for title, info in movies.items() if
            self.filter_movie(info, minimal_rating, start_year,
                              end_year)
        }
        if not filtered_movies:
            print("\nNo movies found matching the criteria.")
        else:
            for title, info in filtered_movies.items():
                year = info.get("year")
                rating = info.get("rating")
                print(f"{title} ({year}): {rating:.1f}")

    def _generate_website(self):
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies to display on the website.")
            return

        with open(os.path.join("_static", "index_template.html"),
                  "r") as template_file:
            template_content = template_file.read()

        movie_grid = ""
        for movie_info in movies.values():
            note = movie_info.get('note', '')
            imdb_id = movie_info.get('imdb_id', '')
            imdb_link = f"https://www.imdb.com/title/{imdb_id}/" \
                if imdb_id else "#"
            movie_grid += f'''
            <li>
                <div class="movie">
                    <a href="{imdb_link}" target="_blank">
                        <img class="movie-poster" src=
                        "{movie_info.get('poster_url')}" alt=
                        "{movie_info.get('title')} poster" 
                        title="{note}">
                    </a>
                    <div class="movie-title"
                    >{movie_info.get('title')}</div>
                    <div class="movie-year"
                    >{movie_info.get('year')}</div>
                    <div class="movie-rating">Rating:
                    {movie_info.get('rating'):.1f}</div>
                </div>
            </li>
            '''

        updated_content = template_content.replace(
            "__TEMPLATE_TITLE__", "My Movie Collection")
        updated_content = updated_content.replace(
            "__TEMPLATE_MOVIE_GRID__", movie_grid)

        with (open(os.path.join("_static", "index.html"), "w") as
              output_file):
            output_file.write(updated_content)

        print("Website was generated successfully.")

    def show_menu(self):
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

    def run(self):
        menu_functions = {
            0: self.exit_program,
            1: self._command_list_movies,
            2: self._command_add_movie,
            3: self._command_delete_movie,
            4: self._command_update_movie,
            5: self._command_movie_stats,
            6: self._command_random_movie,
            7: self._command_search_movie,
            8: self._command_sort_movies_by_rating,
            9: self._command_sort_movies_by_year,
            10: self._command_filter_movies,
            11: self._generate_website,
        }

        print("********** My Movies Database **********")
        while True:
            self.show_menu()
            try:
                choice = int(input("\nEnter choice (0-11): ").strip())
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
            input("\nPress enter to continue")

    def exit_program(self):
        print("\nBye!")

    def get_add_movie_info(self):
        """Prompt the user to enter movie title to add"""
        while True:
            title = input("\nEnter new movie name: ").strip()
            if not title:
                print("\nInput cannot be empty, please try again.")
                continue
            formatted_title = self.format_title(title)
            if formatted_title in self._storage.list_movies():
                print(f"\nMovie {formatted_title} already exist!")
                return None, None, None, None
            movie_data = make_api_request(formatted_title)
            if movie_data and movie_data.get("Response") == "True":
                movie_title = movie_data.get("Title")
                year = movie_data.get("Year")
                rating = movie_data.get("imdbRating")
                poster_url = movie_data.get("Poster")
                imdb_id = movie_data.get("imdbID")
                if year != "N/A":
                    year = int(year)
                else:
                    year = 0
                if rating != "N/A":
                    rating = float(rating)
                else:
                    rating = 0.0
                return movie_title, year, rating, poster_url, imdb_id
            else:
                print("\nCould not find the movie in the OMDb "
                      "database, please try again.")

    def get_update_movie_info(self):
        """Prompt the user to enter movie title and add notes"""
        title = input("\nEnter movie name: ").strip()
        formatted_title = self.format_title(title)
        if formatted_title in self._storage.list_movies():
            note = input("\nEnter movie notes: ").strip()
            return formatted_title, note
        print(f"\nMovie \"{title}\" doesn't exist!")
        return None, None

    def get_delete_movie_info(self):
        """Prompt the user to enter movie title to delete"""
        while True:
            title = input("\nEnter movie name to delete: ").strip()
            if not title:
                print("\nInput cannot be empty, please try again.")
                continue
            formatted_title = self.format_title(title)
            if formatted_title in self._storage.list_movies():
                return formatted_title
            print(f"\nMovie \"{title}\" doesn't exist!")
            return None

    def format_title(self, title):
        """Format the input title to be consistent with the
        database"""
        words = title.split()
        formatted_words = []
        for word in words:
            if word.lower().endswith("'s"):
                formatted_word = word[:-2].capitalize() + "'s"
            else:
                formatted_word = word.capitalize()
            formatted_words.append(formatted_word)
        return " ".join(formatted_words)

    def get_minimal_rating(self):
        """Prompt the user to enter a minimal rating"""
        while True:
            user_input = input(
                "\nEnter minimum rating (leave blank for "
                "no minimum rating): ").strip()
            if not user_input:
                return None
            try:
                rating = float(user_input)
                if 0 <= rating <= 10:
                    return rating
                print("\nPlease enter a rating between 0 and 10.")
            except ValueError:
                print(
                    "\nInvalid input. Please enter a valid rating.")

    def get_start_year(self):
        """Prompt the user to enter a start year"""
        while True:
            user_input = input(
                "\nEnter start year (leave blank for no "
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

    def get_end_year(self):
        """Prompt the user to enter an end year"""
        while True:
            user_input = input(
                "\nEnter end year (leave blank for no "
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

    def filter_movie(self, movie_info, minimal_rating=None,
                     start_year=None,
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

    def calc_average_rating(self, movies=None):
        """Calculate and return the average rating"""
        if movies is None:
            movies = self._storage.list_movies()
        valid_movies = [movie for movie in movies.values() if
                        movie.get("rating") > 0]
        if not valid_movies:
            return 0
        total_ratings = sum(movie["rating"] for movie in valid_movies)
        return total_ratings / len(valid_movies)

    def get_median_rating(self, sorted_movies):
        """Get and return the median of the ratings"""
        ratings = [movie_info["rating"] for movie_info in
                   sorted_movies.values() if movie_info["rating"] > 0]
        if not ratings:
            return 0
        ratings.sort()
        middle = len(ratings) // 2
        if len(ratings) % 2 == 0:
            return (ratings[middle - 1] + ratings[middle]) / 2
        return ratings[middle]

    def get_sort_order(self):
        """Prompt the user for sort order and return True if latest
        first, else False"""
        while True:
            choice = input("\nDo you want the latest movie first?"
                           " (Y/N): ").strip().lower()
            if choice in ['y', 'n']:
                return choice == 'y'
            print("\nPlease enter 'Y' or 'N'.")

    def sort_movies_by_rating(self):
        """Return a sorted dictionary of movies by rating"""
        movies = self._storage.list_movies()
        return dict(sorted(movies.items(), key=lambda item: item[
            1].get("rating", 0), reverse=True))

    def print_sorted_movies_by_rating(self):
        """Print the sorted movies by rating"""
        sorted_movies = self.sort_movies_by_rating()
        if not sorted_movies:
            print("\nNo movies in the database to sort by rating.")
            return
        for movie_title, movie_info in sorted_movies.items():
            print(f'{movie_title}: {movie_info["rating"]:.1f}')
