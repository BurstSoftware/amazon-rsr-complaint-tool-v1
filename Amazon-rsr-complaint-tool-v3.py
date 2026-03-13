import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Anonymous Workplace Experience Form",
    page_icon="📝",
    layout="centered"
)

LOCATION = "Amazon RSR – 2225 Carlson Drive, North Mankato, MN 56003"

STAFF_NAMES = [
    "Ken L. - BH - UTR"
]

st.title("📝 Anonymous Experience / Complaint Form")

st.caption(
    "Use this app to compile your complaint and use the copy functionality "
    "to copy the report of the complaint and paste it into your text messaging "
    "service or your email service to send directly to your supervisor."
)

st.write(
    "This tool allows associates to anonymously document workplace experiences "
    "using the Amazon STAR problem-solving method."
)

st.info(f"Location: {LOCATION}")

# Session storage
if "reports" not in st.session_state:
    st.session_state.reports = []

with st.form("experience_form"):

    person = st.selectbox(
        "Who is this complaint about?",
        STAFF_NAMES
    )

    st.markdown("### Amazon STAR Method")

    situation = st.text_area(
        "Situation",
        help="Describe the context or situation."
    )

    task = st.text_area(
        "Task",
        help="What responsibility or expectation existed?"
    )

    action = st.text_area(
        "Action",
        help="What actions were taken by the person involved?"
    )

    result = st.text_area(
        "Result",
        help="What was the outcome or impact?"
    )

    comments = st.text_area(
        "Additional comments (optional)"
    )

    submitted = st.form_submit_button("Submit Anonymously")

if submitted:

    if situation.strip() == "":
        st.warning("Please provide at least the Situation before submitting.")
    else:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_text = f"""
ANONYMOUS EXPERIENCE REPORT

Location:
{LOCATION}

Complaint About:
{person}

Date Submitted:
{timestamp}

STAR REPORT

Situation:
{situation}

Task:
{task}

Action:
{action}

Result:
{result}

Additional Comments:
{comments}
"""

        report_data = {
            "timestamp": timestamp,
            "person": person,
            "situation": situation,
            "task": task,
            "action": action,
            "result": result,
            "comments": comments,
            "formatted": report_text
        }

        st.session_state.reports.append(report_data)

        st.success("Your complaint report has been compiled.")

        st.subheader("📋 Copy Your Report")

        st.code(report_text)

        st.download_button(
            "Download Report",
            report_text,
            file_name="star_report.txt"
        )

st.divider()

st.header("📊 Session Reports")

report_count = len(st.session_state.reports)

st.metric("Reports Compiled This Session", report_count)

if report_count > 0:

    df = pd.DataFrame(st.session_state.reports)

    st.dataframe(
        df[["timestamp", "person"]],
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
        file_name="all_star_reports.txt"
    )
else:
    st.info("No reports compiled yet.")
