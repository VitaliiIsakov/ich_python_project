import ui
import mysqldb
import log_writer
import log_stats
import formatter

def show_search_results(search_fn, conn, *args, log_info=None):
    """
    Shows search results with pagination.
    Logs the first query if needed.
    """
    offset = 0
    limit = 10

    while True:
        results, headers, total = search_fn(conn, *args, offset, limit)

        # Log only the first query
        if offset == 0 and log_info:
            log_writer.log_search(log_info[0], log_info[1], total)

        if not results:
            print("No results found.")
            return

        print(f"\nShowing {offset + 1} - {offset + len(results)} of {total}")
        formatter.print_table(results, headers)

        offset += limit
        if offset >= total:
            print("All results are shown.")
            return

        answer = input("Show next page? (y/n): ").strip().lower()
        if answer != 'y':
            return


def perform_action(action, conn):
    """
    Executes the user-selected action.
    """
    if action == 1:
        keyword = ui.movie_name()
        show_search_results(
            mysqldb.search_movies_by_keyword,
            conn,
            keyword,
            log_info=("keyword", {"keyword": keyword})
        )

    elif action == 2:
        genre = ui.movie_genre(conn)
        year_mode = ui.year_mode_selection()

        if year_mode == 1:
            year = ui.specific_year(conn)
            show_search_results(
                mysqldb.search_movies_by_genre_and_year_exact,
                conn,
                genre, year,
                log_info=("genre+exact_year", {"genre": genre, "year": year})
            )
        else:
            year_from, year_to = ui.release_year_range(conn)
            show_search_results(
                mysqldb.search_movies_by_genre_or_year,
                conn,
                genre, year_from, year_to,
                log_info=("genre+year_range", {"genre": genre, "from": year_from, "to": year_to})
            )

    elif action == 3:
        print("Popular queries:")
        top = log_stats.get_top_queries()
        formatter.print_table(top, headers=["Params", "Count"])

    elif action == 4:
        print("Recent unique queries:")
        recent = log_stats.get_last_queries()
        formatted = [
            (str(q["params"]), q["timestamp"].strftime("%Y-%m-%d %H:%M:%S"), q.get("results_count"))
            for q in recent
        ]
        formatter.print_table(formatted, headers=["Params", "Timestamp", "Results Count"])

    else:
        print("Invalid choice.")


def menu(conn):
    """
    Main menu of the program.
    """
    while True:
        action = ui.main_menu()
        if action == 0:
            print("Exiting the program.")
            break
        perform_action(action, conn)


def main():
    """
    Starts the program.
    """
    conn = mysqldb.connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    try:
        menu(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
