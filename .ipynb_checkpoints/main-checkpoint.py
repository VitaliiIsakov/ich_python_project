import ui
import mysqldb
import settings
import log_writer
import log_stats
import formatter

def paginate_search(results_fn, conn, *args, log_info=None):
    """
    Displays paginated search results and optionally logs the first query.

    Args:
        results_fn: A function that takes (conn, *args, offset, limit) and returns (results, headers, total_count).
        conn: A MySQL connection object.
        *args: Arguments to pass to the results_fn.
        log_info: Optional tuple (query_type, params) for logging the first query.
    """ 
    offset = 0
    limit = 10
    first = True

    while True:
        results, headers, total = results_fn(conn, *args, offset, limit)
        if first and log_info:
            log_writer.log_search(log_info[0], log_info[1], total)
        first = False

        if not results:
            print("No results found.")
            return

        print(f"\nShowing {offset+1}-{offset+len(results)} of {total}")
        formatter.print_table(results, headers)

        offset += limit
        if offset >= total:
            print("\nAll results shown.")
            return

        if input("Show next page? (y/n): ").lower() != 'y':
            return
        

def action_result(action, mysqldb_conn):
    """
    Executes the selected user action.

    Args:
        action: User-selected action identifier.
        mysqldb_conn: A MySQL connection object.
    """
    if action == 1:
        name = ui.movie_name()
        paginate_search(
            mysqldb.search_movies_by_keyword,
            mysqldb_conn, name,
            log_info=("keyword", {"keyword": name})
        )

    elif action == 2:
        genre = ui.movie_genre(mysqldb_conn)
        year_mode = ui.year_mode_selection()

        if year_mode == 1:
            year = ui.specific_year(mysqldb_conn)
            paginate_search(
                mysqldb.search_movies_by_genre_and_year_exact,
                mysqldb_conn,
                genre, year,
                log_info=("genre+exact_year", {"genre": genre, "year": year})
            )
        else:
            year_from, year_to = ui.release_year_range(mysqldb_conn)
            paginate_search(
                mysqldb.search_movies_by_genre_or_year,
                mysqldb_conn,
                genre, year_from, year_to,
                log_info=("genre+year_range", {"genre": genre, "from": year_from, "to": year_to})
            )

    elif action == 3:
        print("Popular requests:")
        top = log_stats.get_top_queries()
        formatter.print_table(top, headers=["Params", "Count"])

    elif action == 4:
        print("Recent unique requests:")
        recent = log_stats.get_last_queries()
        formatted = [
            (
                str(q["params"]),
                q["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                q.get("results_count")
            )
            for q in recent
        ]
        formatter.print_table(formatted, headers=["Params", "Timestamp", "Results Count"])
    else:
        print("Incorrect input")


def menu(mysqldb_conn):
    """
    Displays the main menu and handles user input until exit.

    Args:
        mysqldb_conn: A MySQL connection object.
    """
    while (action := ui.main_menu()) != 0:
        action_result(action, mysqldb_conn)
        
def main():
    """
    Entry point of the application. Establishes DB connection and starts the menu.
    """
    try:
        mysqldb_conn = mysqldb.connection()
        if not mysqldb_conn:
            print("Failed to connect to MySQL. Exiting.")
            return

    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return

    try:
        menu(mysqldb_conn)
    finally:
        mysqldb_conn.close()
if __name__ == '__main__':
    main()
