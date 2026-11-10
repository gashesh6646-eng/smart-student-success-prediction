
import pandas as pd
import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "student_model.pkl"

# Step 1: Load dataset
df = pd.read_csv(BASE_DIR / "dataset.csv")

# Step 2: Select input features
X = df[[
    "attendance",
    "previous_marks",
    "assignment_marks",
    "study_hours"
]]

# Step 3: Select output
y = df["status"]

# Step 4: Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Step 5: Create ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Step 6: Train model
model.fit(X_train, y_train)

# Step 7: Test model
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Model trained successfully!")
print("Model Accuracy:", accuracy * 100, "%")

# Confusion Matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Step 8: Save trained model
with open(MODEL_PATH, "wb") as file:
    pickle.dump(model, file)

print("\nML Model saved successfully!")
