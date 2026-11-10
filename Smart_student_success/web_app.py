import pickle
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent


@st.cache_resource
def load_model():
    with open(BASE_DIR / "student_model.pkl", "rb") as model_file:
        return pickle.load(model_file)


st.set_page_config(page_title="Smart Student Success", page_icon="📚")
st.title("Smart Student Success")
st.caption("Machine learning based student performance prediction")
st.info(
    "This public demo keeps records only for the active visitor session. "
    "Do not enter sensitive student information."
)

if "records" not in st.session_state:
    st.session_state.records = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None

with st.form("student_prediction"):
    name = st.text_input("Student label (use an alias)")
    attendance = st.number_input(
        "Attendance (%)", min_value=0.0, max_value=100.0, value=75.0
    )
    previous_marks = st.number_input(
        "Previous marks", min_value=0.0, max_value=100.0, value=60.0
    )
    assignment_marks = st.number_input(
        "Assignment marks", min_value=0.0, max_value=100.0, value=60.0
    )
    study_hours = st.number_input(
        "Daily study hours", min_value=0.0, value=2.0, step=0.5
    )
    submitted = st.form_submit_button("Predict student success")

if submitted:
    if not name.strip():
        st.error("Please enter a label or alias.")
    else:
        student_data = pd.DataFrame(
            [
                {
                    "attendance": attendance,
                    "previous_marks": previous_marks,
                    "assignment_marks": assignment_marks,
                    "study_hours": study_hours,
                }
            ]
        )
        prediction = load_model().predict(student_data)[0]
        record = {
            "Name": name.strip(),
            "Attendance (%)": attendance,
            "Previous marks": previous_marks,
            "Assignment marks": assignment_marks,
            "Study hours": study_hours,
            "Prediction": prediction,
        }
        st.session_state.records.append(record)
        st.session_state.last_result = record

result = st.session_state.last_result
if result is not None:
    if result["Prediction"] == "Pass":
        st.success(f'Prediction for {result["Name"]}: Pass')
    else:
        st.warning(f'Prediction for {result["Name"]}: {result["Prediction"]}')

    recommendations = []
    if result["Attendance (%)"] < 75:
        recommendations.append("Improve attendance to at least 75%.")
    if result["Previous marks"] < 50:
        recommendations.append("Focus more on previous subject topics.")
    if result["Assignment marks"] < 50:
        recommendations.append("Complete assignments regularly.")
    if result["Study hours"] < 2:
        recommendations.append("Increase daily study hours.")
    if not recommendations and result["Prediction"] == "Pass":
        recommendations.append("Good performance! Keep it up.")
    if not recommendations:
        recommendations.append("Continue working consistently.")
    st.markdown("**Recommendations**")
    for recommendation in recommendations:
        st.write(f"- {recommendation}")

if st.session_state.records:
    records_df = pd.DataFrame(st.session_state.records)
    st.subheader("Records in this session")
    st.dataframe(
        records_df.assign(**{"No.": range(1, len(records_df) + 1)}).set_index("No.")
    )

    pass_count = (records_df["Prediction"] == "Pass").sum()
    at_risk_count = len(records_df) - pass_count
    total_col, pass_col, risk_col = st.columns(3)
    total_col.metric("Total students", len(records_df))
    pass_col.metric("Pass", int(pass_count))
    risk_col.metric("At Risk", int(at_risk_count))

    status_counts = records_df["Prediction"].value_counts()
    st.bar_chart(status_counts)
