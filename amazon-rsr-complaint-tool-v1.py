import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Anonymous Workplace Feedback", page_icon="📝")

st.title("📝 Anonymous Workplace Experience Form")

st.write("""
This form allows associates to anonymously document experiences about a process assistant.
No names, logins, or identifying information are collected.
""")

LOCATION = "Amazon RSR – 2225 Carlson Drive, North Mankato, MN 56003"

st.info(f"Location: {LOCATION}")

file_name = "feedback_data.csv"

# Create file if missing
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=[
        "timestamp",
        "experience",
        "rating",
        "additional_comments"
    ])
    df.to_csv(file_name, index=False)


with st.form("anonymous_form"):

    experience = st.text_area(
        "Describe your experience:",
        height=180,
        placeholder="Write what happened..."
    )

    rating = st.slider(
        "Experience rating",
        1,
        5,
        3
    )

    comments = st.text_area(
        "Additional comments (optional)"
    )

    submit = st.form_submit_button("Submit Anonymously")


if submit:

    if experience.strip() == "":
        st.warning("Please describe your experience before submitting.")
    else:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_entry = pd.DataFrame({
            "timestamp": [timestamp],
            "experience": [experience],
            "rating": [rating],
            "additional_comments": [comments]
        })

        new_entry.to_csv(file_name, mode="a", header=False, index=False)

        st.success("Your anonymous experience has been saved.")

        # Create formatted version for copying
        formatted_text = f"""
ANONYMOUS EXPERIENCE REPORT
Location: {LOCATION}

Date Submitted: {timestamp}

Experience Rating: {rating}/5

Experience Description:
{experience}

Additional Comments:
{comments}
"""

        st.subheader("📋 Copy Your Saved Report")

        st.write("You can copy this report and paste it into a text message, email, or document.")

        st.code(formatted_text)

        st.download_button(
            "Download Report as TXT",
            formatted_text,
            file_name="experience_report.txt"
        )


st.divider()

st.subheader("📊 Anonymous Submission Count")

try:
    data = pd.read_csv(file_name)
    st.metric("Total Reports Submitted", len(data))
except:
    st.write("No submissions yet.")
