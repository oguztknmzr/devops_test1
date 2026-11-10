import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host=os.getenv("DB_HOST", "localhost"),  # change if needed
        port="5432",  # change if needed
    )


def create_tables():
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS authors (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    country VARCHAR(50)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    year INTEGER,
                    author_id INTEGER REFERENCES authors(id) ON DELETE CASCADE
                );
            """)
    connection.close()
    print("Tables created successfully.")


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
