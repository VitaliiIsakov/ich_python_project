import mysqldb
import formatter

def main_menu() -> int:
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
            val = int(choice)
            if val in [0,1,2,3,4]:
                return val
        except ValueError:
            pass
        print("Please enter a number between 0 and 4.")

def movie_name() -> str:
    return input('Enter movie name or keyword >>> ')

def movie_genre(conn) -> str:
    genres = mysqldb.get_all_genres(conn)
    print("Available genres:", ", ".join(genres))
    return input("Choose a genre: ")

def year_mode_selection() -> int:
    while True:
        print("1 - Specific year\n2 - Year range")
        choice = input("Enter 1 or 2: ")
        if choice in ('1','2'):
            return int(choice)
        print("Please enter 1 or 2.")

def specific_year(conn) -> int:
    min_y, max_y = mysqldb.get_year_range(conn)
    print(f"Available years: {min_y} - {max_y}")
    while True:
        try:
            y = int(input("Enter year: "))
            if min_y <= y <= max_y:
                return y
        except ValueError:
            pass
        print("Invalid year.")

def release_year_range(conn):
    min_y, max_y = mysqldb.get_year_range(conn)
    print(f"Available years: {min_y} - {max_y}")
    while True:
        try:
            y1 = int(input("From year: "))
            y2 = int(input("To year: "))
            if min_y <= y1 <= y2 <= max_y:
                return y1, y2
        except ValueError:
            pass
        print("Invalid range.")

def show_no_results():
    print("No results found.")

def show_page_info(offset, count, total):
    print(f"\nShowing {offset+1}-{offset+count} of {total}")

def ask_next_page() -> bool:
    ans = input("Show next page? (y/n): ").strip().lower()
    return ans == 'y'

def show_end_of_results():
    print("All results are shown.")

def display_table(data, headers=None):
    formatter.print_table(data, headers)

def show_popular_queries(queries):
    headers = ["#", "Query", "Count"]
    rows = [(i, q, c) for i,(q,c) in enumerate(queries,1)]
    formatter.print_table(rows, headers)

def show_recent_queries(recent):
    headers = ["#", "Params", "Timestamp", "Results Count"]
    rows = [
        (i, str(q["params"]), q["timestamp"].strftime("%Y-%m-%d %H:%M:%S"), q["results_count"])
        for i,q in enumerate(recent,1)
    ]
    formatter.print_table(rows, headers)

def show_invalid_choice():
    print("Invalid choice.")

def show_exit_message():
    print("Exiting the program.")

def show_connection_error():
    print("Failed to connect to the database.")