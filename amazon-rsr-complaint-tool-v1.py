import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Anonymous Workplace Experience Form",
    page_icon="📝",
    layout="centered"
)

LOCATION = "Amazon RSR – 2225 Carlson Drive, North Mankato, MN 56003"

st.title("📝 Anonymous Experience Form")

st.write(
    "This tool allows associates to anonymously record workplace experiences. "
    "No identifying information is collected."
)

st.info(f"Location: {LOCATION}")

# Initialize session storage
if "reports" not in st.session_state:
    st.session_state.reports = []

with st.form("experience_form"):

    experience = st.text_area(
        "Describe your experience",
        height=180,
        placeholder="Explain what happened..."
    )

    rating = st.slider(
        "Experience Rating",
        1,
        5,
        3
    )

    comments = st.text_area(
        "Additional comments (optional)"
    )

    submitted = st.form_submit_button("Submit Anonymously")

if submitted:

    if experience.strip() == "":
        st.warning("Please describe your experience before submitting.")
    else:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_text = f"""
ANONYMOUS EXPERIENCE REPORT
Location: {LOCATION}

Date Submitted: {timestamp}

Experience Rating: {rating}/5

Experience Description:
{experience}

Additional Comments:
{comments}
"""

        report_data = {
            "timestamp": timestamp,
            "rating": rating,
            "experience": experience,
            "comments": comments,
            "formatted": report_text
        }

        st.session_state.reports.append(report_data)

        st.success("Your anonymous experience has been saved.")

        st.subheader("📋 Copy Your Report")

        st.code(report_text)

        st.download_button(
            "Download Report",
            report_text,
            file_name="experience_report.txt"
        )

st.divider()

st.header("📊 Session Reports")

report_count = len(st.session_state.reports)

st.metric("Reports Submitted This Session", report_count)

if report_count > 0:

    df = pd.DataFrame(st.session_state.reports)

    st.dataframe(
        df[["timestamp", "rating"]],
        use_container_width=True
    )

    st.subheader("📋 Copy All Reports")

    all_reports_text = "\n\n----------------------------\n\n".join(
        r["formatted"] for r in st.session_state.reports
    )

    st.code(all_reports_text)

    st.download_button(
        "Download All Reports",
        all_reports_text,
        file_name="all_experience_reports.txt"
    )
else:
    st.info("No reports submitted yet.")
