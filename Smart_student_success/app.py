import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sqlite3
import pickle
import subprocess
import sys
from pathlib import Path

from database import DATABASE_PATH, initialize_database

BASE_DIR = Path(__file__).resolve().parent

initialize_database()

# Load trained ML model
with open(BASE_DIR / "student_model.pkl", "rb") as file:
    model = pickle.load(file)


# Prediction function
def predict_student():

    name = name_entry.get().strip()

    try:
        attendance = float(attendance_entry.get())
        previous_marks = float(previous_entry.get())
        assignment_marks = float(assignment_entry.get())
        study_hours = float(hours_entry.get())

        if not name:
            messagebox.showerror("Error", "Please enter student name!")
            return

        if not all(0 <= x <= 100 for x in
                   [attendance, previous_marks, assignment_marks]):
            messagebox.showerror("Error", "Marks and attendance must be between 0 and 100!")
            return

        if study_hours < 0:
            messagebox.showerror("Error", "Study hours cannot be negative!")
            return

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values!")
        return

    # Prepare student data
    student_data = pd.DataFrame([{
        "attendance": attendance,
        "previous_marks": previous_marks,
        "assignment_marks": assignment_marks,
        "study_hours": study_hours
    }])

    # Predict result
    prediction = model.predict(student_data)[0]

    # Save in database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name, attendance, previous_marks,
    assignment_marks, study_hours, predicted_status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name, attendance, previous_marks,
        assignment_marks, study_hours, prediction
    ))

    conn.commit()
    conn.close()
    # Display prediction
    result_label.config(
        text="Prediction: " + prediction,
        fg="green" if prediction == "Pass" else "red"
    )

    # Generate improvement recommendations
    recommendations = []

    if attendance < 75:
        recommendations.append("Improve attendance to at least 75%.")

    if previous_marks < 50:
        recommendations.append("Focus more on previous subject topics.")

    if assignment_marks < 50:
        recommendations.append("Complete assignments regularly.")

    if study_hours < 2:
        recommendations.append("Increase daily study hours.")

    if prediction == "Pass" and not recommendations:
        recommendations.append("Good performance! Keep it up.")

    if not recommendations:
        recommendations.append("Continue working consistently.")

    recommendation_label.config(
        text="Recommendations:\n" + "\n".join(
            "- " + item for item in recommendations
        )
    )

    messagebox.showinfo(
        "Success",
        "Student prediction completed!\nRecord saved in database."
    )


# Clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    attendance_entry.delete(0, tk.END)
    previous_entry.delete(0, tk.END)
    assignment_entry.delete(0, tk.END)
    hours_entry.delete(0, tk.END)
    result_label.config(text="Prediction: Not Available", fg="black")
    recommendation_label.config(text="Recommendations: Not Available")


# View database records
def view_records():

    window = tk.Toplevel(root)
    window.title("Student Records")
    window.geometry("1100x400")

    columns = (
        "No.", "Database ID", "Name", "Attendance", "Previous Marks",
        "Assignment Marks", "Study Hours", "Status"
    )

    table = ttk.Treeview(
        window, columns=columns, show="headings"
    )

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100, anchor="center")
    table.column("Name", width=150)

    table.pack(fill="both", expand=True)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students ORDER BY id ASC")
    records = cursor.fetchall()

    conn.close()

    for row_number, record in enumerate(records, start=1):
        table.insert("", tk.END, values=(row_number, *record))


def delete_student_record(student_id):
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_student():
    window = tk.Toplevel(root)
    window.title("Delete Student")
    window.geometry("500x400")

    table = ttk.Treeview(
        window,
        columns=("Student No.", "Database ID", "Name"),
        show="headings"
    )
    for column, width in (
        ("Student No.", 90), ("Database ID", 100), ("Name", 240)
    ):
        table.heading(column, text=column)
        table.column(column, width=width, anchor="center")
    table.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_records():
        table.delete(*table.get_children())
        try:
            with sqlite3.connect(DATABASE_PATH) as conn:
                records = conn.execute(
                    "SELECT id, name FROM students ORDER BY id ASC"
                ).fetchall()
        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load student records:\n{error}",
                parent=window
            )
            return

        for row_number, (student_id, name) in enumerate(records, start=1):
            table.insert(
                "",
                tk.END,
                iid=str(student_id),
                values=(row_number, student_id, name)
            )

    def delete_selected():
        selection = table.selection()
        if not selection:
            messagebox.showwarning(
                "No Student Selected",
                "Select a student to delete.",
                parent=window
            )
            return

        row_number, _, name = table.item(selection[0], "values")
        student_id = selection[0]
        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Delete student No. {row_number}: {name}?\n"
            f"(Database ID: {student_id})",
            parent=window
        ):
            return

        try:
            deleted = delete_student_record(int(student_id))
        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not delete the student record:\n{error}",
                parent=window
            )
            return

        if not deleted:
            messagebox.showwarning(
                "Record Not Found",
                "That student record no longer exists.",
                parent=window
            )
            refresh_records()
            return

        refresh_records()
        messagebox.showinfo(
            "Deleted",
            f"The record for {name} was deleted.",
            parent=window
        )

    tk.Button(
        window,
        text="Delete Selected Student",
        command=delete_selected
    ).pack(pady=(0, 10))
    refresh_records()


# Open dashboard
def open_dashboard():
    subprocess.Popen([sys.executable, str(BASE_DIR / "dashboard.py")])


# Main application window
root = tk.Tk()
root.title("Smart Student Success Prediction System")
root.geometry("750x700")
root.configure(bg="#EAF2F8")

# Heading
heading = tk.Label(
    root,
    text="SMART STUDENT SUCCESS",
    font=("Arial", 22, "bold"),
    bg="#EAF2F8",
    fg="#154360"
)
heading.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Machine Learning Based Student Performance Prediction",
    font=("Arial", 11),
    bg="#EAF2F8"
)
subtitle.pack(pady=5)


# Input frame
frame = tk.Frame(root, bg="white", padx=30, pady=20)
frame.pack(pady=20)

def add_field(label, row):
    tk.Label(
        frame, text=label,
        font=("Arial", 11, "bold"),
        bg="white"
    ).grid(row=row, column=0, padx=10, pady=12, sticky="w")

    entry = tk.Entry(frame, font=("Arial", 12), width=25)
    entry.grid(row=row, column=1, padx=10, pady=12)

    return entry


name_entry = add_field("Student Name:", 0)
attendance_entry = add_field("Attendance (%):", 1)
previous_entry = add_field("Previous Marks:", 2)
assignment_entry = add_field("Assignment Marks:", 3)
hours_entry = add_field("Daily Study Hours:", 4)


# Predict button
tk.Button(
    root,
    text="PREDICT STUDENT SUCCESS",
    font=("Arial", 12, "bold"),
    bg="#2471A3",
    fg="white",
    width=30,
    command=predict_student
).pack(pady=10)


# Result label
result_label = tk.Label(
    root,
    text="Prediction: Not Available",
    font=("Arial", 15, "bold"),
    bg="#EAF2F8"
)
result_label.pack(pady=10)

recommendation_label = tk.Label(
    root,
    text="Recommendations: Not Available",
    font=("Arial", 10),
    bg="#EAF2F8",
    justify="left",
    wraplength=650
)
recommendation_label.pack(pady=5)


# Other buttons
button_frame = tk.Frame(root, bg="#EAF2F8")
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="Clear Fields",
    width=15,
    command=clear_fields
).grid(row=0, column=0, padx=8)

tk.Button(
    button_frame,
    text="View Records",
    width=15,
    command=view_records
).grid(row=0, column=1, padx=8)

tk.Button(
    button_frame,
    text="Open Dashboard",
    width=15,
    command=open_dashboard
).grid(row=0, column=2, padx=8)

tk.Button(
    button_frame,
    text="Delete Student",
    width=15,
    command=delete_student
).grid(row=0, column=3, padx=8)


# Start application
if __name__ == "__main__":
    root.mainloop()