# 1) Search movies by keyword with pagination
query_movies_by_keyword = """
    SELECT title, release_year, description
    FROM film
    WHERE title LIKE %s
    LIMIT %s OFFSET %s
"""

# Count total movies matching a keyword
query_count_movies_by_keyword = """
    SELECT COUNT(*)
    FROM film
    WHERE title LIKE %s
"""

# 2) Search movies by genre and year range with pagination
query_movies_by_genre_or_year = """
    SELECT f.title, f.release_year, c.name AS genre
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s
      AND f.release_year BETWEEN %s AND %s
    LIMIT %s OFFSET %s
"""

# Count total movies by genre and year range
query_count_movies_by_genre_or_year = """
    SELECT COUNT(*)
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s
      AND f.release_year BETWEEN %s AND %s
"""

# 3) Search movies by genre and exact year with pagination
query_movies_by_genre_and_year_exact = """
    SELECT f.title, f.release_year, c.name AS genre
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s
      AND f.release_year = %s
    LIMIT %s OFFSET %s
"""

# Count total movies by genre and exact year
query_count_movies_by_genre_and_year_exact = """
    SELECT COUNT(*)
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s
      AND f.release_year = %s
"""

# Get all genres
query_genres = "SELECT name FROM category"

# Get min and max release years
query_years = """
    SELECT MIN(release_year), MAX(release_year)
    FROM film
"""