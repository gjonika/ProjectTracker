
import streamlit as st
import json
import os
from datetime import datetime
from components.project_dashboard_ui import render_project_dashboard_ui
from utils.data_loader import load_projects_from_json
# App title
st.set_page_config(page_title="Project Tracker", layout="centered")
st.title("📋 Personal Project Tracker")

# Paths to JSON files
PROJECTS_FILE = "data/projects.json"
ACTIVITY_FILE = "data/activity_log.json"


tabs = st.tabs(["📥 Import CSV", "📋 View Projects"])

with tabs[0]:
    st.subheader("📥 Import Projects from CSV")

    # Download Template
    with open("data/sample_template.csv", "rb") as f:
        st.download_button("📄 Download CSV Template", f, "project_template.csv")

    # Upload CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file:
    from utils.data_loader import import_projects_from_csv

    try:
        count = import_projects_from_csv(uploaded_file)
        st.success(f"✅ Imported {count} projects!")
    except Exception as e:
        st.error(f"❌ Failed to import: {e}")



with tabs[1]:
    json_path = "data/projects.json"

    if os.path.exists(json_path):
        projects = load_projects_from_json(json_path)

        if not projects:
            st.info("No projects to display yet.")
        else:
            render_project_dashboard_ui(projects)
    else:
        st.warning("⚠️ No projects.json file found. Please import a CSV first.")

# Load/save helpers
def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# Load project and activity data
projects = load_json(PROJECTS_FILE)
activity_log = load_json(ACTIVITY_FILE)



# --- New Project Form ---
with st.expander("➕ Add New Project"):
    with st.form("new_project_form"):
        name = st.text_input("Project Name*", "")
        description = st.text_area("Description", "")
        ptype = st.selectbox("Type", ["Personal", "For Sale"])
        status = st.selectbox("Status", ["Idea", "In Progress", "Live", "Abandoned"])
        stage = st.selectbox("Stage", ["Idea", "Build", "Market", "Launch"])
        usefulness = st.select_slider("Usefulness", options=[1, 2, 3, 4, 5], value=3)
        monetized = st.checkbox("Monetized 💰")
        github_url = st.text_input("GitHub URL")
        next_action = st.text_input("Next Action")

        submitted = st.form_submit_button("Create Project")
        if submitted and name:
            new_project = {
                "id": len(projects) + 1,
                "name": name,
                "description": description,
                "type": ptype,
                "status": status,
                "stage": stage,
                "usefulness": usefulness,
                "monetized": monetized,
                "github_url": github_url,
                "next_action": next_action,
                "created": datetime.now().isoformat()
            }
            projects.append(new_project)
            save_json(PROJECTS_FILE, projects)

            activity_log.append({
                "action": "Created Project",
                "project": name,
                "timestamp": datetime.now().isoformat()
            })
            save_json(ACTIVITY_FILE, activity_log)
            st.success("✅ Project created!")

# --- Project List Display ---
st.subheader("📁 All Projects")
if projects:
    for proj in reversed(projects):
        st.markdown(f"### {proj['name']}")
        st.markdown(f"**Status:** `{proj['status']}` | **Stage:** `{proj['stage']}` | **Type:** `{proj['type']}`")
        st.progress(proj['usefulness'] * 0.2)
        st.markdown(f"**Description:** {proj['description'] or '_No description_'}")
        if proj['next_action']:
            st.markdown(f"**Next Action:** _{proj['next_action']}_")
        if proj['github_url']:
            st.markdown(f"[GitHub ↗]({proj['github_url']})")
        st.markdown("---")
else:
    st.info("No projects yet. Add your first one above!")

# --- Activity Log ---
with st.expander("🕓 Activity Log"):
    if activity_log:
        for log in reversed(activity_log):
            st.markdown(f"- {log['timestamp'][:19]} → **{log['action']}**: `{log['project']}`")
    else:
        st.write("No activity yet.")
