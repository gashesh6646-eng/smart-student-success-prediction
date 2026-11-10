import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

data = {
    "attendance": [95, 85, 70, 50, 40, 90, 60, 75, 88, 45,
                   92, 65, 55, 80, 35, 96, 72, 58, 84, 48],

    "previous_marks": [90, 78, 65, 40, 30, 88, 45, 70, 82, 35,
                       92, 55, 42, 75, 25, 95, 60, 38, 80, 32],

    "assignment_marks": [95, 80, 68, 45, 35, 90, 50, 72, 85, 40,
                         96, 60, 48, 78, 30, 98, 65, 42, 82, 36],

    "study_hours": [4, 3, 2, 1, 0.5, 4, 1.5, 2.5, 3, 1,
                    5, 2, 1, 3, 0.5, 5, 2.5, 1, 3.5, 0.5]
}

df = pd.DataFrame(data)

# Demo labels for learning purposes
score = (
    df["attendance"] * 0.25
    + df["previous_marks"] * 0.35
    + df["study_hours"] * 3
)

df["status"] = score.apply(
    lambda x: "Pass" if x >= 48 else "At Risk"
)

df.to_csv(BASE_DIR / "dataset.csv", index=False)

print("Student dataset created successfully!")
print(df.head())