import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Anonymous Workplace Experience Form",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
    <style>
    .main {padding-top: 2rem;}
    .stButton button {width: 100%; border-radius: 8px; height: 42px;}
    .section-header {font-size: 1.4rem; font-weight: 600; margin: 1.5rem 0 0.8rem 0;}
    .report-box {background-color: #f8f9fa; padding: 1.5rem; border-radius: 12px; border: 1px solid #e0e0e0;}
    </style>
""", unsafe_allow_html=True)

LOCATION = "Amazon RSR – 2225 Carlson Drive, North Mankato, MN 56003"

STAFF_NAMES = [
    "Ken L - BH-UTR / RTS", "Eliezt", "David", "Wash", "Omar",
    "Ashely H", "Mike S", "Artur", "Dan"
]

DAYS_OF_WEEK = ["All Reports", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

COMPLAINT_TAGS = [
    "Unequitable treatment towards me", "Special treatment for others", "Lack of communication",
    "Unprofessional behavior", "Harassment or intimidation", "Favoritism", "Unclear expectations",
    "Retaliation concerns", "Unsafe work conditions", "Policy not being followed"
]

# Sidebar
st.sidebar.title("📅 Navigation")
selected_page = st.sidebar.radio("View Reports By Day", DAYS_OF_WEEK, label_visibility="collapsed")

# Header
st.title("📝 Anonymous Experience Form")
st.markdown("**Professional • Confidential • Easy to Use**")
st.caption("Share your workplace experience anonymously. All reports are saved locally in this session.")

st.info(f"**Location:** {LOCATION}", icon="📍")

# Session State
if "reports" not in st.session_state:
    st.session_state.reports = []
if "selected_persons" not in st.session_state:
    st.session_state.selected_persons = []

# ====================== COMPLAINT ABOUT ======================
st.markdown('<p class="section-header">👥 Who is this about?</p>', unsafe_allow_html=True)

# Show selected people
if st.session_state.selected_persons:
    st.success("**Selected:** " + " • ".join(st.session_state.selected_persons))
else:
    st.info("Select one or more people below")

col_ms, col_add = st.columns([3, 2])

with col_ms:
    selected_from_list = st.multiselect(
        "Choose from team members",
        STAFF_NAMES,
        default=[n for n in st.session_state.selected_persons if n in STAFF_NAMES],
        placeholder="Click to select...",
        label_visibility="collapsed"
    )

with col_add:
    new_name = st.text_input("Add someone else", placeholder="Full name / position", label_visibility="collapsed")

if st.button("➕ Add Name", type="secondary", use_container_width=True):
    if new_name.strip():
        name = new_name.strip()
        if name not in st.session_state.selected_persons:
            st.session_state.selected_persons.append(name)
            st.success(f"Added **{name}**")
            st.rerun()
    else:
        st.warning("Please enter a name")

# Sync multiselect
for name in selected_from_list:
    if name not in st.session_state.selected_persons:
        st.session_state.selected_persons.append(name)

# Remove selected people
if st.session_state.selected_persons:
    st.markdown("**Remove:**")
    cols = st.columns(len(st.session_state.selected_persons))
    for i, person in enumerate(st.session_state.selected_persons[:]):
        with cols[i]:
            if st.button(f"❌ {person}", key=f"rm_{i}"):
                st.session_state.selected_persons.remove(person)
                st.rerun()

# ====================== MAIN FORM ======================
with st.form("experience_form", clear_on_submit=False):

    st.markdown('<p class="section-header">📅 When did it happen?</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.date_input("Date", value=datetime.now(), label_visibility="collapsed")
    with col2:
        time_input_str = st.text_input(
            "Time", 
            value=datetime.now().strftime("%H:%M"),
            placeholder="14:30 or 2:30 PM",
            label_visibility="collapsed"
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
    st.success(f"**Incident Day:** {day_of_week}, {selected_date.strftime('%B %d, %Y')}")

    if time_error:
        st.error("Invalid time format. Use HH:MM or HH:MM AM/PM")

    st.markdown('<p class="section-header">⚠️ What concerns apply?</p>', unsafe_allow_html=True)
    selected_tags = st.multiselect("Select all that apply", COMPLAINT_TAGS, label_visibility="collapsed")

    st.markdown('<p class="section-header">📋 STAR Method</p>', unsafe_allow_html=True)
    
    situation = st.text_area("**Situation**", placeholder="What happened?", height=120)
    task = st.text_area("**Task**", placeholder="What was your responsibility?", height=100)
    action = st.text_area("**Action**", placeholder="What did you do?", height=100)
    result = st.text_area("**Result**", placeholder="What was the outcome?", height=100)
    comments = st.text_area("Additional Comments (optional)", height=100)

    submitted = st.form_submit_button("🚀 Submit Report Anonymously", type="primary", use_container_width=True)

# ====================== SUBMISSION ======================
if submitted:
    if not st.session_state.selected_persons:
        st.error("Please select at least one person.")
    elif not situation.strip():
        st.warning("Please describe the **Situation**.")
    elif time_error:
        st.warning("Please fix the time format.")
    else:
        # Build report
        persons_text = ", ".join(st.session_state.selected_persons)
        tags_text = ", ".join(selected_tags) if selected_tags else "None"

        incident_time = datetime.combine(selected_date, parsed_time)
        incident_str = incident_time.strftime("%A, %B %d, %Y at %I:%M %p")
        submitted_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        report_text = f"""ANONYMOUS WORKPLACE EXPERIENCE REPORT

Location: {LOCATION}

Complaint About: {persons_text}

Incident: {incident_str}
Submitted: {submitted_str}

Concerns: {tags_text}

=== STAR REPORT ===
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
            "incident_date": selected_date.strftime("%B %d, %Y"),
            "incident_time": incident_str,
            "submitted_time": submitted_str,
            "person": persons_text,
            "tags": selected_tags,
            "formatted": report_text
        }

        st.session_state.reports.append(report_data)

        st.success("**Report Submitted Successfully!**", icon="✅")
        st.subheader("📋 Your Report")
        st.code(report_text, language=None)

        st.download_button(
            "⬇️ Download Report",
            report_text,
            file_name=f"experience_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            use_container_width=True
        )

# ====================== REPORTS SECTION ======================
st.divider()
st.header(f"📊 {selected_page} Reports")

reports = st.session_state.reports
filtered = [r for r in reports if selected_page == "All Reports" or r["day_of_week"] == selected_page]

st.metric("Total Reports", len(filtered))

if filtered:
    df = pd.DataFrame(filtered)
    st.dataframe(
        df[["incident_date", "incident_time", "person"]],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("All Reports")
    combined = "\n\n" + "═"*80 + "\n\n".join(r["formatted"] for r in filtered)
    st.code(combined, language=None)

    st.download_button(
        f"⬇️ Download All {selected_page} Reports",
        combined,
        file_name=f"{selected_page.lower()}_reports.txt",
        use_container_width=True
    )
else:
    st.info("No reports submitted yet for this day.", icon="📭")
