import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "student_success.db"


def initialize_database():
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            attendance REAL,
            previous_marks REAL,
            assignment_marks REAL,
            study_hours REAL,
            predicted_status TEXT
        )
        """)


if __name__ == "__main__":
    initialize_database()
    print("Database is ready!")