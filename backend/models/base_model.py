from backend.database import get_db

def fetch_all(table):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
