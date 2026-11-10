import pandas as pd
import pickle
import sqlite3
from pathlib import Path

from database import initialize_database

BASE_DIR = Path(__file__).resolve().parent
initialize_database()

# Load trained ML model
with open(BASE_DIR / "student_model.pkl", "rb") as file:
    model = pickle.load(file)

print("SMART STUDENT SUCCESS PREDICTION SYSTEM")

# Take student information
name = input("Enter student name: ")

attendance = float(input("Enter attendance percentage: "))
previous_marks = float(input("Enter previous exam marks: "))
assignment_marks = float(input("Enter assignment marks: "))
study_hours = float(input("Enter daily study hours: "))

# Prepare input for prediction
student_data = pd.DataFrame([{
    "attendance": attendance,
    "previous_marks": previous_marks,
    "assignment_marks": assignment_marks,
    "study_hours": study_hours
}])

# Predict student status
prediction = model.predict(student_data)[0]

print("\nStudent Name:", name)
print("Predicted Status:", prediction)

# Connect to database
conn = sqlite3.connect(BASE_DIR / "student_success.db")
cursor = conn.cursor()

# Save student information and prediction
cursor.execute("""
INSERT INTO students
(name, attendance, previous_marks, assignment_marks,
study_hours, predicted_status)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    name,
    attendance,
    previous_marks,
    assignment_marks,
    study_hours,
    prediction
))

conn.commit()
conn.close()

print("\nStudent record saved in database!")