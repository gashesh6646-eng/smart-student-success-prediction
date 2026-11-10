import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

from database import initialize_database

BASE_DIR = Path(__file__).resolve().parent
initialize_database()

# Connect to database
conn = sqlite3.connect(BASE_DIR / "student_success.db")

# Read student records
df = pd.read_sql_query("SELECT * FROM students", conn)

conn.close()

# Check database records
if df.empty:
    print("No student records found!")
else:
    print("===== STUDENT PERFORMANCE DASHBOARD =====")

    print("Total Students:", len(df))
    print("Pass Students:", (df["predicted_status"] == "Pass").sum())
    print("At Risk Students:", (df["predicted_status"] == "At Risk").sum())

    # Graph 1: Pass vs At Risk
    status_count = df["predicted_status"].value_counts()

    plt.figure(figsize=(7, 5))
    status_count.plot(kind="bar")

    plt.title("Pass vs At Risk Students")
    plt.xlabel("Student Status")
    plt.ylabel("Number of Students")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # Graph 2: Student Attendance
    plt.figure(figsize=(8, 5))

    plt.bar(df["name"], df["attendance"])

    plt.title("Student Attendance Comparison")
    plt.xlabel("Student Name")
    plt.ylabel("Attendance Percentage")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()

    # Graph 3: Marks Comparison
    plt.figure(figsize=(8, 5))

    plt.plot(df["name"], df["previous_marks"],
             marker="o", label="Previous Marks")

    plt.plot(df["name"], df["assignment_marks"],
             marker="o", label="Assignment Marks")

    plt.title("Student Marks Comparison")
    plt.xlabel("Student Name")
    plt.ylabel("Marks")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\nDashboard generated successfully!")