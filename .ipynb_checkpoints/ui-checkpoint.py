import mysqldb
import formatter
import typing

def main_menu() -> int:
    """
    Displays the main menu and returns the user's selected action as an integer.

    Returns:
        int: A number from 0 to 4 representing the user's selected action.
    """
    while True:
        print("""
        Menu:
        1 - Search by movie name
        2 - Search by genre and year
        3 - Show popular search queries
        4 - Show recent unique queries
        0 - Exit
        """)
        choice = input("Enter your choice: ")
        try:
            action = int(choice)
            if action in [0, 1, 2, 3, 4]:
                return action
            else:
                print("Please enter a number between 0 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def movie_name() ->str:
    """
    Prompts the user to input a movie name or keyword.

    Returns:
        str: The user input as a keyword or name.
    """
    return input('Input movie name or keyword>>>')

def movie_genre(conn) ->str:
    """
    Prompts the user to select a genre from the available genres.

    Args:
        conn: A database connection object.

    Returns:
        str: The selected genre.
    """
    genres = mysqldb.get_all_genres(conn)
    print("Available genres:", ", ".join(genres))
    return input("Choose genre: ")

def year_mode_selection() ->int:
    """
    Prompts the user to choose between a specific year or a year range.

    Returns:
        int: 1 for specific year, 2 for year range.
    """
    while True:
        print("Choose year search mode:")
        print("1. Specific year")
        print("2. Year range")
        choice = input("Enter 1 or 2: ")
        try:
            choice_int = int(choice)
            if choice_int in (1, 2):
                return choice_int
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number (1 or 2).")

def specific_year(conn) -> int:
    """
    Prompts the user to enter a specific year within the valid range.

    Args:
        conn: A database connection object.

    Returns:
        int: The selected year.
    """
    min_year, max_year = mysqldb.get_year_range(conn)
    print(f"Available years: {min_year} - {max_year}")
    while True:
        try:
            year = int(input("Enter year: "))
            if min_year <= year <= max_year:
                return year
            print("Year out of range.")
        except ValueError:
            print("Invalid input.")
    
def release_year_range(conn) ->typing.Tuple[int, int]:
    """
    Prompts the user to input a valid year range.

    Args:
        conn: A database connection object.

    Returns:
        Tuple[int, int]: The selected year range as (from_year, to_year).
    """
    min_year, max_year = mysqldb.get_year_range(conn)
    print(f"Available years: {min_year} - {max_year}")
    while True:
        try:
            from_year = int(input("From year: "))
            to_year = int(input("To year: "))
            if min_year <= from_year <= to_year <= max_year:
                return from_year, to_year
            print("Invalid range.")
        except ValueError:
            print("Invalid input.")

def print_table_data(data, headers=None):
    """
    Prints the most popular queries with their counts.

    Args:
        queries: A list of tuples (query_str, count).
    """
    formatter.print_table(data, headers=headers)

def print_top_queries(queries: list[tuple]):
    """
    Prints a list of recent unique queries with additional metadata.

    Args:
        queries: A list of dictionaries representing recent queries.
    """
    headers = ["#", "Query", "Count"]
    table_data = [(i, q, count) for i, (q, count) in enumerate(queries, 1)]
    formatter.print_table(table_data, headers=headers)

def print_recent_queries(queries: list[dict]):
    """
    Prints a list of recent unique queries with additional metadata.

    Args:
        queries: A list of dictionaries representing recent queries.
    """
    headers = ["#", "Search Type", "Params", "Timestamp", "Results Count"]
    table_data = [
        (
            i,
            q.get("search_type", ""),
            q.get("params", ""),
            q.get("timestamp", ""),
            q.get("results_count", "")
        )
        for i, q in enumerate(queries, 1)
    ]
    print_table_data(table_data, headers=headers)