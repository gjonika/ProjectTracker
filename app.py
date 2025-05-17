import streamlit as st
import os
import json
from datetime import datetime
from components.project_dashboard_ui import render_project_dashboard_ui
from utils.data_loader import load_projects_from_json, import_projects_from_csv

st.set_page_config(page_title="Project Tracker", layout="centered")

# Light luxury theme
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFDF4 !important;  /* Ivory background */
        color: #434A54 !important;
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #1A237E;
    }

    .stButton>button {
        background-color: #1A237E !important;
        color: white !important;
        border-radius: 6px;
        padding: 0.4rem 1rem;
        font-weight: 600;
        border: none;
    }

    .stButton>button:hover {
        background-color: #FFD700 !important;
        color: black !important;
    }

    .stTextInput>div>div>input,
    .stSelectbox>div>div,
    .stRadio>div>label {
        background-color: white !important;
        color: #1A237E !important;
        border-radius: 6px;
        border: 1px solid #ccc;
    }

    .st-expander > summary {
        font-weight: bold;
        color: #1A237E;
    }

    .stProgress > div > div > div {
        background-color: #1A237E !important;
    }

    .stAlert {
        border-left: 6px solid #FFD700;
    }

    .css-1v3fvcr { /* Tag pills */
        background-color: #FFD700 !important;
        color: black !important;
        font-weight: 500;
        border-radius: 12px;
        padding: 0.2rem 0.6rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)



PROJECTS_FILE = "data/projects.json"
TEMPLATE_CSV = "data/sample_template.csv"

tabs = st.tabs(["📥 Import CSV", "📋 View Projects"])

# --- TAB 1: Import CSV ---
with tabs[0]:
    st.subheader("📥 Import Projects from CSV")

    # Download Template
    with open(TEMPLATE_CSV, "rb") as f:
        st.download_button("📄 Download CSV Template", f, "project_template.csv")

    # Upload CSV
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
            render_project_dashboard_ui(projects)
    else:
        st.warning("⚠️ No projects.json file found. Please import a CSV first.")
