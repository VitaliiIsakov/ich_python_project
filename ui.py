import mysqldb
import formatter
import typing

def main_menu() -> int:
    """
    Show the main menu and get the user's choice.
    Returns:
        int: Number from 0 to 4 based on user input.
    """
    while True:
        print("""
        Menu:
        1 - Search by movie name
        2 - Search by genre and year
        3 - Show popular searches
        4 - Show recent unique searches
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
            print("Invalid input. Please enter a number.")

def movie_name() -> str:
    """
    Ask the user to type a movie name or keyword.
    Returns:
        str: The user's input.
    """
    return input('Enter movie name or keyword >>> ')

def movie_genre(conn) -> str:
    """
    Show available genres and ask the user to pick one.
    Args:
        conn: Database connection.
    Returns:
        str: Chosen genre.
    """
    genres = mysqldb.get_all_genres(conn)
    print("Available genres:", ", ".join(genres))
    return input("Choose a genre: ")

def year_mode_selection() -> int:
    """
    Ask if the user wants to search by a specific year or by a range.
    Returns:
        int: 1 for specific year, 2 for year range.
    """
    while True:
        print("Choose year search mode:")
        print("1. Specific year")
        print("2. Year range")
        choice = input("Enter 1 or 2: ")
        try:
            val = int(choice)
            if val in (1, 2):
                return val
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")

def specific_year(conn) -> int:
    """
    Ask the user to enter a year inside the valid range.
    Args:
        conn: Database connection.
    Returns:
        int: The year entered by the user.
    """
    min_year, max_year = mysqldb.get_year_range(conn)
    print(f"Available years: {min_year} - {max_year}")
    while True:
        try:
            year = int(input("Enter year: "))
            if min_year <= year <= max_year:
                return year
            print("Year is out of range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def release_year_range(conn) -> typing.Tuple[int, int]:
    """
    Ask the user to enter a valid year range.
    Args:
        conn: Database connection.
    Returns:
        tuple: (start_year, end_year)
    """
    min_year, max_year = mysqldb.get_year_range(conn)
    print(f"Available years: {min_year} - {max_year}")
    while True:
        try:
            from_year = int(input("From year: "))
            to_year = int(input("To year: "))
            if min_year <= from_year <= to_year <= max_year:
                return from_year, to_year
            print("Invalid year range.")
        except ValueError:
            print("Invalid input. Please enter numbers.")

def print_table_data(data, headers=None):
    """
    Print data as a table.
    Args:
        data: List of rows to print.
        headers: List of column names.
    """
    formatter.print_table(data, headers=headers)

def print_top_queries(queries: list[tuple]):
    """
    Print popular search queries with counts.
    Args:
        queries: List of (query, count) tuples.
    """
    headers = ["#", "Query", "Count"]
    table_data = [(i, q, c) for i, (q, c) in enumerate(queries, 1)]
    formatter.print_table(table_data, headers=headers)

def print_recent_queries(queries: list[dict]):
    """
    Print recent unique queries with details.
    Args:
        queries: List of dicts with query info.
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