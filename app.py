import streamlit as st
import json
import os
from datetime import datetime
from uuid import uuid4

# ---------- File Paths ----------
PROJECTS_FILE = "data/projects.json"
ACTIVITY_FILE = "data/activity_log.json"

# ---------- Load or Init Data ----------
def load_data(path, default=[]):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return default

def save_data(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)



projects = load_data(PROJECTS_FILE)
activity_log = load_data(ACTIVITY_FILE)

# ---------- Sidebar ----------
st.sidebar.title("📌 Project Filters")
status_filter = st.sidebar.selectbox("Filter by Status", ["All", "idea", "in progress", "live", "abandoned"])
if st.sidebar.button("➕ Add New Project"):
    st.session_state.show_form = True

# ---------- Main Header ----------
st.title("🧠 Project Tracker")

# ---------- Add Project Form ----------
if st.session_state.get("show_form"):
    with st.form("add_project", clear_on_submit=True):
        st.subheader("Create a New Project")
        name = st.text_input("Name*", placeholder="e.g., AI Writing Assistant")
        description = st.text_input("Description", placeholder="Short description")
        p_type = st.selectbox("Type", ["Personal", "For Sale"])
        status = st.selectbox("Status", ["idea", "in progress", "live", "abandoned"])
        stage = st.selectbox("Stage", ["Idea", "Build", "Market", "Launch"])
        usefulness = st.select_slider("Usefulness", options=[1,2,3,4,5], value=3)
        monetized = st.checkbox("Monetized 💰")
        github_url = st.text_input("GitHub URL")
        next_action = st.text_input("Next Action")

        submitted = st.form_submit_button("✅ Create Project")
        if submitted and name:
            new_project = {
                "id": str(uuid4()),
                "name": name,
                "description": description,
                "type": p_type,
                "status": status,
                "stage": stage,
                "usefulness": usefulness,
                "monetized": monetized,
                "github_url": github_url,
                "next_action": next_action,
                "progress": 0,
                "last_updated": datetime.now().isoformat()
            }
            projects.append(new_project)
            activity_log.append({
                "timestamp": datetime.now().isoformat(),
                "event": f"Created project '{name}'"
            })
            save_data(PROJECTS_FILE, projects)
            save_data(ACTIVITY_FILE, activity_log)
            st.success("Project added!")
            st.session_state.show_form = False
            st.experimental_rerun()

# ---------- Project Cards ----------
filtered_projects = [
    p for p in projects if status_filter == "All" or p["status"] == status_filter
]

for project in filtered_projects:
    with st.container():
        st.subheader(project["name"])
        st.caption(project["description"])
        st.markdown(
            f"""
            **Status:** `{project["status"]}`  
            **Stage:** `{project["stage"]}`  
            **Type:** `{project["type"]}`  
            **Monetized:** {'✅' if project["monetized"] else '❌'}  
            **Next Action:** {project["next_action"] or '—'}  
            """
        )
        st.progress(project["progress"] / 100)
        if project["github_url"]:
            st.markdown(f"[GitHub]({project['github_url']})")

        with st.expander("📜 Activity Log"):
            for entry in activity_log:
                if project["name"] in entry["event"]:
                    st.write(f"{entry['timestamp'][:19]} - {entry['event']}")
        st.divider()
