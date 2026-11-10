import sqlite3
from pathlib import Path

from database import initialize_database

BASE_DIR = Path(__file__).resolve().parent
initialize_database()

# Connect to database
conn = sqlite3.connect(BASE_DIR / "student_success.db")
cursor = conn.cursor()

# Display all students
cursor.execute("SELECT id, name, predicted_status FROM students")
records = cursor.fetchall()

print("\n===== STUDENT RECORDS =====")

if not records:
    print("No student records found.")

else:
    for record in records:
        print(
            "ID:", record[0],
            "| Name:", record[1],
            "| Status:", record[2]
        )

    # Ask for student ID
    student_id = input("\nEnter ID of student to delete: ")

    if student_id.isdigit():

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (int(student_id),)
        )

        if cursor.rowcount > 0:
            conn.commit()
            print("\nStudent record deleted successfully!")
        else:
            print("\nStudent ID not found.")

    else:
        print("\nPlease enter a valid ID.")

conn.close()