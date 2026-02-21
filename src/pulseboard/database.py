import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "pulseboard.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chart_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            value INTEGER NOT NULL
        )
    """)

    # Seed data if empty
    cursor.execute("SELECT COUNT(*) FROM chart_data")
    if cursor.fetchone()[0] == 0:
        seed_data = [("Jan", 10), ("Feb", 25), ("Mar", 40), ("Apr", 35)]
        cursor.executemany(
            "INSERT INTO chart_data (label, value) VALUES (?, ?)", seed_data
        )

    conn.commit()
    conn.close()
