import sqlite3
import os


def db_connect(query: str) -> list[tuple]:
    """
    Connects to the database and returns a list of tuples.

    :param query:
    :return:
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))
    index = base_dir.find('src')
    db_path = base_dir[:index] + 'data/db/emotions.db'

    # db 연결
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        finally:
            cursor.close()

    return result
