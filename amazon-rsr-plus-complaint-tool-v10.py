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
    "Ken L - BH-UTR / RTS",
    "Eliezt",
    "David",
    "Wash",
    "Omar",
    "Ashely H",
    "Mike S",
    "Artur",
    "Dan"
]

DAYS_OF_WEEK = ["All Reports", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

COMPLAINT_TAGS = [
    "Unequitable treatment towards me", "Special treatment for others", "Lack of communication",
    "Unprofessional behavior", "Harassment or intimidation", "Favoritism", "Unclear expectations",
    "Retaliation concerns", "Unsafe work conditions", "Policy not being followed"
]

# Sidebar
st.sidebar.title("📅 Select Day")
selected_page = st.sidebar.radio("Go to:", DAYS_OF_WEEK)

st.title("📝 Anonymous Experience / Complaint Form")
st.caption("Use this app to compile your complaint and copy/send it to your supervisor.")
st.info(f"Location: {LOCATION}")

# Session State
if "reports" not in st.session_state:
    st.session_state.reports = []
if "selected_persons" not in st.session_state:
    st.session_state.selected_persons = []   # Now a list for multi-select

# ====================== MULTI NAME SELECTION ======================
st.markdown("### 👥 Who is this complaint about? (You can select multiple)")

# Show currently selected people
if st.session_state.selected_persons:
    st.success("**Selected:** " + ", ".join(st.session_state.selected_persons))
else:
    st.info("Select staff members below")

# Multi-select for existing staff
selected_from_list = st.multiselect(
    "Select from existing staff:",
    STAFF_NAMES,
    default=[name for name in st.session_state.selected_persons if name in STAFF_NAMES],
    key="multi_staff"
)

# Add custom name
st.markdown("**Add a name not in the list:**")
col1, col2 = st.columns([4, 1])
with col1:
    new_name = st.text_input("Enter name", placeholder="e.g. John Smith - Lead", key="new_name_input")
with col2:
    if st.button("➕ Add Name", type="secondary", key="add_name_btn"):
        if new_name.strip():
            if new_name.strip() not in st.session_state.selected_persons:
                st.session_state.selected_persons.append(new_name.strip())
                st.success(f"Added: {new_name.strip()}")
                st.rerun()
            else:
                st.warning("This name is already added.")
        else:
            st.warning("Please enter a name")

# Sync multiselect with session state
if selected_from_list:
    for name in selected_from_list:
        if name not in st.session_state.selected_persons:
            st.session_state.selected_persons.append(name)

# Remove button for selected people
if st.session_state.selected_persons:
    st.markdown("**Currently Selected:**")
    remove_cols = st.columns(len(st.session_state.selected_persons))
    for idx, person in enumerate(st.session_state.selected_persons):
        with remove_cols[idx]:
            if st.button(f"❌ {person}", key=f"remove_{idx}"):
                st.session_state.selected_persons.remove(person)
                st.rerun()

# ====================== FORM SECTION ======================
with st.form("experience_form"):

    st.markdown("### 📅 Incident Timing")

    selected_date = st.date_input("Select the date of the incident", value=datetime.now())

    time_input_str = st.text_input(
        "Enter time (e.g., 14:30 or 2:30 PM)",
        value=datetime.now().strftime("%H:%M")
    )

    # Time parsing
    parsed_time = None
    time_error = False
    try:
        try:
            parsed_time = datetime.strptime(time_input_str, "%H:%M").time()
        except:
            parsed_time = datetime.strptime(time_input_str, "%I:%M %p").time()
    except:
        time_error = True

    day_of_week = selected_date.strftime("%A")
    st.success(f"📅 This incident occurred on: **{day_of_week}**")

    if time_error:
        st.error("⛔ Invalid time format. Use HH:MM (24hr) or HH:MM AM/PM")

    # Tags
    st.markdown("### ⚠️ Select Applicable Concerns")
    selected_tags = st.multiselect("Choose any that apply:", COMPLAINT_TAGS)

    if selected_tags:
        st.write("**Selected Concerns:**")
        st.write(" • " + "\n • ".join(selected_tags))

    st.markdown("### Amazon STAR Method")
    situation = st.text_area("Situation")
    task = st.text_area("Task")
    action = st.text_area("Action")
    result = st.text_area("Result")
    comments = st.text_area("Additional comments (optional)")

    submitted = st.form_submit_button("Submit Anonymously", type="primary")

# ====================== SUBMISSION LOGIC ======================
if submitted:
    if not st.session_state.selected_persons:
        st.error("⚠️ Please select at least one person before submitting.")
    elif situation.strip() == "":
        st.warning("Please provide at least the **Situation**.")
    elif time_error or parsed_time is None:
        st.warning("Please enter a valid time.")
    else:
        incident_datetime = datetime.combine(selected_date, parsed_time)
        incident_timestamp = incident_datetime.strftime("%A, %B %d, %Y at %I:%M %p")
        incident_date_clean = selected_date.strftime("%B %d, %Y")
        submitted_timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        persons_text = ", ".join(st.session_state.selected_persons)
        selected_tags_text = ", ".join(selected_tags) if selected_tags else "None selected"

        report_text = f"""
ANONYMOUS EXPERIENCE REPORT

Location:
{LOCATION}

Complaint About:
{persons_text}

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

        report_data = {
            "day_of_week": day_of_week,
            "incident_date": incident_date_clean,
            "incident_time": incident_timestamp,
            "submitted_time": submitted_timestamp,
            "person": persons_text,                    # Store as comma-separated string
            "persons_list": st.session_state.selected_persons.copy(),  # Store as list too
            "tags": selected_tags,
            "formatted": report_text
        }

        st.session_state.reports.append(report_data)

        st.success("✅ Report submitted successfully!")
        st.subheader("📋 Copy Your Report")
        st.code(report_text)

        st.download_button("Download Report", report_text, file_name="star_report.txt")

        # Optional: Clear selection after submit
        # st.session_state.selected_persons = []

# ====================== DISPLAY REPORTS ======================
st.divider()
st.header(f"📊 {selected_page}")

reports = st.session_state.reports

if selected_page != "All Reports":
    filtered_reports = [r for r in reports if r["day_of_week"] == selected_page]
else:
    filtered_reports = reports

report_count = len(filtered_reports)
st.metric("Reports Shown", report_count)

if report_count > 0:
    df = pd.DataFrame(filtered_reports)
    st.dataframe(
        df[["day_of_week", "incident_date", "incident_time", "person"]],
        use_container_width=True
    )

    st.subheader("📋 All Reports")
    all_reports_text = "\n\n" + "-"*60 + "\n\n".join(r["formatted"] for r in filtered_reports)
    st.code(all_reports_text)

    st.download_button(
        f"Download {selected_page} Reports",
        all_reports_text,
        file_name=f"{selected_page.lower().replace(' ', '_')}_reports.txt"
    )
else:
    st.info("No reports yet for this selection.")
