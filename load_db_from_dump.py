import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_NAME = "hackathon_db"
DB_USER = "admin"
DB_PASSWORD = "admin#123"
DB_HOST = "localhost"
DB_PORT = "5432"
DUMP_FILE = "manufacturing_core_db.dump"


def create_database_if_not_exists():
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (DB_NAME,)
    )

    if not cur.fetchone():
        print(f"Creating database: {DB_NAME}")
        cur.execute(f"CREATE DATABASE {DB_NAME}")
    else:
        print(f"Database {DB_NAME} already exists")

    cur.close()
    conn.close()


def restore_database():
    print("Restoring database from dump...")
    cmd = [
        "pg_restore",
        "-U", DB_USER,
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-d", DB_NAME,
        "--clean",
        "--if-exists",
        "--no-owner",
    "--no-privileges",
        DUMP_FILE
    ]

    subprocess.run(cmd, check=True)
    print("Restore completed successfully")


if __name__ == "__main__":
    # create_database_if_not_exists()
    restore_database()

#to run this file
# 1) install pip install psycopg2-binary
# 2) export PGPASSWORD=your_password
# 3) python restore_db.py