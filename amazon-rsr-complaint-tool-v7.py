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

DAYS_OF_WEEK = [
    "All Reports",
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

# Complaint Tags
COMPLAINT_TAGS = [
    "Unequitable treatment towards me",
    "Special treatment for others",
    "Lack of communication",
    "Unprofessional behavior",
    "Harassment or intimidation",
    "Favoritism",
    "Unclear expectations",
    "Retaliation concerns",
    "Unsafe work conditions",
    "Policy not being followed"
]

# Sidebar Navigation
st.sidebar.title("📅 Select Day")
selected_page = st.sidebar.radio("Go to:", DAYS_OF_WEEK)

st.title("📝 Anonymous Experience / Complaint Form")

st.caption(
    "Use this app to compile your complaint and copy/send it to your supervisor."
)

st.info(f"Location: {LOCATION}")

# Session storage
if "reports" not in st.session_state:
    st.session_state.reports = []

# =========================
# FORM SECTION
# =========================
with st.form("experience_form"):

    person = st.selectbox(
        "Who is this complaint about?",
        STAFF_NAMES
    )

    st.markdown("### 📅 Incident Timing")

    selected_date = st.date_input(
        "Select the date of the incident",
        value=datetime.now()
    )

    selected_time = st.time_input(
        "Select the time of the incident",
        value=datetime.now().time()
    )

    # Auto derive day of week
    day_of_week = selected_date.strftime("%A")

    st.success(f"📅 This incident occurred on: {day_of_week}")

    # Multi-select tags
    st.markdown("### ⚠️ Select Applicable Concerns")

    selected_tags = st.multiselect(
        "Choose any that apply:",
        COMPLAINT_TAGS
    )

    if selected_tags:
        st.write("### Selected Concerns Preview")
        st.write(" • " + "\n • ".join(selected_tags))

    st.markdown("### Amazon STAR Method")

    situation = st.text_area("Situation")
    task = st.text_area("Task")
    action = st.text_area("Action")
    result = st.text_area("Result")
    comments = st.text_area("Additional comments (optional)")

    submitted = st.form_submit_button("Submit Anonymously")

# =========================
# SUBMISSION LOGIC
# =========================
if submitted:

    if situation.strip() == "":
        st.warning("Please provide at least the Situation before submitting.")
    else:

        incident_datetime = datetime.combine(selected_date, selected_time)

        # ✅ Improved timestamp format
        incident_timestamp = incident_datetime.strftime("%A, %B %d, %Y at %I:%M %p")
        incident_date_clean = selected_date.strftime("%B %d, %Y")

        submitted_timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        selected_tags_text = ", ".join(selected_tags) if selected_tags else "None selected"

        # ✅ Updated report format
        report_text = f"""
ANONYMOUS EXPERIENCE REPORT

Location:
{LOCATION}

Complaint About:
{person}

Incident Day & Time:
{incident_timestamp}

Report Submitted At:
{submitted_timestamp}

Selected Concerns:
{selected_tags_text}

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

        # ✅ Store enhanced data
        report_data = {
            "day_of_week": day_of_week,
            "incident_date": incident_date_clean,
            "incident_time": incident_timestamp,
            "submitted_time": submitted_timestamp,
            "person": person,
            "tags": selected_tags,
            "formatted": report_text
        }

        st.session_state.reports.append(report_data)

        st.success("Report submitted successfully!")

        st.subheader("📋 Copy Your Report")
        st.code(report_text)

        st.download_button(
            "Download Report",
            report_text,
            file_name="star_report.txt"
        )

# =========================
# DISPLAY SECTION
# =========================
st.divider()

st.header(f"📊 {selected_page}")

reports = st.session_state.reports

# Filter logic
if selected_page != "All Reports":
    filtered_reports = [r for r in reports if r["day_of_week"] == selected_page]
else:
    filtered_reports = reports

report_count = len(filtered_reports)

st.metric("Reports Shown", report_count)

if report_count > 0:

    df = pd.DataFrame(filtered_reports)

    # ✅ Updated table view
    st.dataframe(
        df[["day_of_week", "incident_date", "incident_time", "person"]],
        use_container_width=True
    )

    st.subheader("📋 Copy Reports")

    all_reports_text = "\n\n----------------------------\n\n".join(
        r["formatted"] for r in filtered_reports
    )

    st.code(all_reports_text)

    st.download_button(
        f"Download {selected_page} Reports",
        all_reports_text,
        file_name=f"{selected_page.lower().replace(' ', '_')}_reports.txt"
    )

else:
    st.info("No reports for this selection yet.")
