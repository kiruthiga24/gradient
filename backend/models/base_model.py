from backend.database import get_db

def fetch_all(table):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def insert_record(table, data: dict):
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"

    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, list(data.values()))
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result
