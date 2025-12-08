import psycopg2
from psycopg2.extras import DictCursor

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="manufacturing_core_db",
        user="postgres",
        password="admin#123",
        cursor_factory=DictCursor
    )


