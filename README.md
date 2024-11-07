# Movie App

A simple movie management application that allows users to add, delete, update, search, and list movies using different storage options (JSON or CSV). Users can also generate a webpage displaying their movie collection.

## Features
- Add, delete, update, and list movies.
- Store movies in either JSON or CSV format.
- Search movies by title.
- Sort movies by year or rating.
- Filter movies by rating and year range.
- Generate a movie collection webpage.

## Requirements
- Python 3.8+
- Required libraries: see [requirements.txt](#requirements-file)

## Project Structure
```
movie-project/
├── data/                # Storage files (e.g., john.json, ashley.csv)
├── movie_app/           # Core application files
│   ├── __init__.py
│   ├── api.py
│   ├── istorage.py      # Interface for storage classes
│   ├── movie_app.py     # Main application logic
│   ├── storage_csv.py   # CSV storage implementation
│   ├── storage_json.py  # JSON storage implementation
├── static/              # Static HTML template and CSS
├── tests/               # Unit tests for the application
│   ├── __init__.py
│   ├── test_movie_app.py
│   ├── test_storage_csv.py
│   └── test_storage_json.py
├── main.py              # Main entry point for running the application
├── requirements.txt     # Required libraries
└── README.md            # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/movie-project.git
   cd movie-project
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python3 main.py <storage_file>
   ```
   Replace `<storage_file>` with the desired JSON or CSV storage file name (e.g., `john.json` or `ashley.csv`).

4. To run unit tests:
   ```
   python3 -m unittest discover -s tests
   ```

## Usage Examples
- **Add a Movie**: Choose option 2 from the menu and enter the movie details.
- **Delete a Movie**: Choose option 3 and enter the movie title.
- **Generate Website**: Choose option 11 to generate a webpage with your movie collection.

## File Storage Types
- **JSON**: Supports storing and retrieving movie information in a structured JSON format.
- **CSV**: Provides an easy-to-read tabular format for storing movie data.

## Requirements File
- `argparse`
- `requests`
- `unittest`

## Requirements File
See `requirements.txt` for a list of required libraries and dependencies.

## Contributing
Feel free to submit issues or contribute to this project by making pull requests.

## License
This project is licensed under the MIT License.
