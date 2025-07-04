"""
This module helps to connect and query the MySQL database.

Features:
- Connect to MySQL database
- Search movies by keyword
- Search movies by genre and year range or exact year
- Get all available genres
- Get the minimum and maximum release years
"""

import pymysql
import settings
import queries
from typing import List, Tuple, Optional


def connection() -> Optional[pymysql.connections.Connection]:
    """
    Connect to the MySQL database using settings from settings.py.

    Returns:
        Connection object if successful, else None.
    """
    try:
        conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DB
        )
        return conn
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def search_movies_by_keyword(
    conn: pymysql.connections.Connection,
    keyword: str,
    offset: int = 0,
    limit: int = 10
) -> Tuple[List[dict], List[str], int]:
    """
    Find movies with titles containing the keyword.

    Args:
        conn: MySQL connection
        keyword: Text to search in titles
        offset: Skip this many records (for pagination)
        limit: Max records to return

    Returns:
        (list of movie rows, list of column names, total matching count)
    """
    with conn.cursor() as cursor:
        cursor.execute(
            queries.query_movies_by_keyword,
            (f"%{keyword}%", limit, offset)
        )
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description] if rows else []

        cursor.execute(
            queries.query_count_movies_by_keyword,
            (f"%{keyword}%",)
        )
        total_count = cursor.fetchone()[0]

        return rows, headers, total_count


def search_movies_by_genre_or_year(
    conn: pymysql.connections.Connection,
    genre: str,
    year_from: int,
    year_to: int,
    offset: int = 0,
    limit: int = 10
) -> Tuple[List[dict], List[str], int]:
    """
    Find movies matching a genre or released between years.

    Args:
        conn: MySQL connection
        genre: Genre to filter
        year_from: Start year
        year_to: End year
        offset: Skip records
        limit: Max records

    Returns:
        (list of movie rows, list of column names, total count)
    """
    with conn.cursor() as cursor:
        cursor.execute(
            queries.query_movies_by_genre_or_year,
            (genre, year_from, year_to, limit, offset)
        )
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description] if rows else []

        cursor.execute(
            queries.query_count_movies_by_genre_or_year,
            (genre, year_from, year_to)
        )
        total_count = cursor.fetchone()[0]

        return rows, headers, total_count


def search_movies_by_genre_and_year_exact(
    conn: pymysql.connections.Connection,
    genre: str,
    year: int,
    offset: int = 0,
    limit: int = 10
) -> Tuple[List[dict], List[str], int]:
    """
    Find movies with exact genre and release year.

    Args:
        conn: MySQL connection
        genre: Genre filter
        year: Exact year filter
        offset: Skip records
        limit: Max records

    Returns:
        (list of movie rows, list of column names, total count)
    """
    with conn.cursor() as cursor:
        cursor.execute(
            queries.query_movies_by_genre_and_year_exact,
            (genre, year, limit, offset)
        )
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description] if rows else []

        cursor.execute(
            queries.query_count_movies_by_genre_and_year_exact,
            (genre, year)
        )
        total_count = cursor.fetchone()[0]

        return rows, headers, total_count


def get_all_genres(conn: pymysql.connections.Connection) -> List[str]:
    """
    Get all movie genres from the database.

    Args:
        conn: MySQL connection

    Returns:
        List of genre names
    """
    with conn.cursor() as cursor:
        cursor.execute(queries.query_genres)
        rows = cursor.fetchall()
        return [row[0] for row in rows] if rows else []


def get_year_range(conn: pymysql.connections.Connection) -> Tuple[int, int]:
    """
    Get the earliest and latest movie release years.

    Args:
        conn: MySQL connection

    Returns:
        (min_year, max_year) or (0, 0) if no data
    """
    with conn.cursor() as cursor:
        cursor.execute(queries.query_years)
        result = cursor.fetchone()
        if result:
            return result[0], result[1]
        return 0, 0