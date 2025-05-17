import streamlit as st
import os
import json
from datetime import datetime
from components.project_dashboard_ui import render_project_dashboard_ui
from utils.data_loader import load_projects_from_json, import_projects_from_csv

st.set_page_config(page_title="Project Tracker", layout="wide")

PROJECTS_FILE = "data/projects.json"
TEMPLATE_CSV = "data/sample_template.csv"

# Load external CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("theme.css")

# --- Top Button Bar + View Mode Toggle ---
st.title("📋 Project Dashboard")

buttons = st.columns([1, 1, 1, 1, 2])
with buttons[0]:
    st.button("➕ Add Project")
with buttons[1]:
    st.button("📥 Import CSV")
with buttons[2]:
    st.button("📤 Export JSON")
with buttons[3]:
    st.button("📤 Export CSV")
with buttons[4]:
    view_mode = st.radio("View", ["Grid", "List"], horizontal=True, label_visibility="collapsed")

# --- Page Tabs ---
tabs = st.tabs(["📥 Import CSV", "📋 View Projects"])

# --- TAB 1: Import CSV ---
with tabs[0]:
    st.subheader("📥 Import Projects from CSV")

    with open(TEMPLATE_CSV, "rb") as f:
        st.download_button("📄 Download CSV Template", f, "project_template.csv")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        try:
            count = import_projects_from_csv(uploaded_file, json_path=PROJECTS_FILE)
            st.success(f"✅ Imported {count} projects!")
        except Exception as e:
            st.error(f"❌ Failed to import: {e}")

# --- TAB 2: View Projects ---
with tabs[1]:
    st.subheader("📋 My Projects")

    if os.path.exists(PROJECTS_FILE):
        projects = load_projects_from_json(PROJECTS_FILE)

        if not projects:
            st.info("No projects to display yet.")
        else:
            if view_mode == "Grid":
                cols = st.columns(3)
                for i, project in enumerate(projects):
                    with cols[i % 3]:
                        with st.container():
                            st.markdown(render_project_dashboard_ui(project), unsafe_allow_html=True)
            else:
                for project in projects:
                    with st.container():
                        st.markdown(render_project_dashboard_ui(project), unsafe_allow_html=True)
    else:
        st.warning("⚠️ No projects.json file found. Please import a CSV first.")
