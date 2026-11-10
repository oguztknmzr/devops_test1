from psycopg2.extras import RealDictCursor
from db_setup import get_connection


def get_authors():
    connection = get_connection()
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM authors ORDER BY id;")
            result = cursor.fetchall()
    connection.close()
    return result


def get_author(author_id):
    connection = get_connection()
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM authors WHERE id = %s;", (author_id,))
            result = cursor.fetchone()
    connection.close()
    return result


def add_author(name, country):
    connection = get_connection()
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO authors (name, country) VALUES (%s, %s) RETURNING *;",
                (name, country),
            )
            result = cursor.fetchone()
    connection.close()
    return result


def update_author(author_id, name, country):
    connection = get_connection()
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE authors SET name = %s, country = %s WHERE id = %s RETURNING *;",
                (name, country, author_id),
            )
            result = cursor.fetchone()
    connection.close()
    return result


def delete_author(author_id):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM authors WHERE id = %s RETURNING id;", (author_id,))
            result = cursor.fetchone()
    connection.close()
    return result

def get_books():
    connection = get_connection()
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM books ORDER BY id;")
            result = cursor.fetchall()
    connection.close()
    return result


def get_book(book_id):
    connection = get_connection()
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM books WHERE id = %s;", (book_id,))
            result = cursor.fetchone()
    connection.close()
    return result


def add_book(title, year, author_id):
    connection = get_connection()
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO books (title, year, author_id) VALUES (%s, %s, %s) RETURNING *;",
                (title, year, author_id),
            )
            result = cursor.fetchone()
    connection.close()
    return result


def update_book(book_id, title, year, author_id):
    connection = get_connection()
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE books SET title = %s, year = %s, author_id = %s WHERE id = %s RETURNING *;",
                (title, year, author_id, book_id),
            )
            result = cursor.fetchone()
    connection.close()
    return result


def delete_book(book_id):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM books WHERE id = %s RETURNING id;", (book_id,))
            result = cursor.fetchone()
    connection.close()
    return result
