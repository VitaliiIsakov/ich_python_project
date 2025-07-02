import ui
import mysqldb
import log_writer
import log_stats
import formatter

def show_search_results(search_fn, conn, *args, log_info=None):
    offset = 0
    limit = 10
    first = True

    while True:
        results, headers, total = search_fn(conn, *args, offset, limit)

        if first and log_info:
            search_type, params = log_info
            log_writer.log_search(search_type, params, total)
        first = False

        if not results:
            ui.show_no_results()
            return

        ui.show_page_info(offset, len(results), total)
        ui.display_table(results, headers)

        offset += limit
        if offset >= total:
            ui.show_end_of_results()
            return

        if not ui.ask_next_page():
            return

def perform_action(action, conn):
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
        mode = ui.year_mode_selection()
        if mode == 1:
            year = ui.specific_year(conn)
            show_search_results(
                mysqldb.search_movies_by_genre_and_year_exact,
                conn,
                genre, year,
                log_info=("genre+exact_year", {"genre": genre, "year": year})
            )
        else:
            y1, y2 = ui.release_year_range(conn)
            show_search_results(
                mysqldb.search_movies_by_genre_or_year,
                conn,
                genre, y1, y2,
                log_info=("genre+year_range", {"genre": genre, "from": y1, "to": y2})
            )
    elif action == 3:
        top = log_stats.get_top_queries()
        ui.show_popular_queries(top)
    elif action == 4:
        recent = log_stats.get_last_queries()
        ui.show_recent_queries(recent)
    else:
        ui.show_invalid_choice()

def menu(conn):
    while True:
        action = ui.main_menu()
        if action == 0:
            ui.show_exit_message()
            break
        perform_action(action, conn)

def main():
    conn = mysqldb.connection()
    if not conn:
        ui.show_connection_error()
        return
    try:
        menu(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
