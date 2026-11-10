import sqlite3
import pandas as pd
from pathlib import Path

from database import initialize_database

BASE_DIR = Path(__file__).resolve().parent
initialize_database()

# Connect to database
conn = sqlite3.connect(BASE_DIR / "student_success.db")

# Fetch all student records in ID order
query = "SELECT * FROM students ORDER BY id ASC"

df = pd.read_sql_query(query, conn)

# Close connection
conn.close()

# Display records
print("\n===== STUDENT DATABASE RECORDS =====\n")

if df.empty:
    print("No student records found.")
else:
    df.insert(0, "No.", range(1, len(df) + 1))

    print(df.to_string(index=False))

print("\nTotal Students:", len(df))