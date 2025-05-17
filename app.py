import streamlit as st
from utils.data_loader import import_projects_from_csv, save_projects_to_json
import os
import tempfile

st.set_page_config(page_title="Project Tracker", layout="centered")

st.title("📥 Import Projects from CSV")

# Upload CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.getvalue())
        temp_path = tmp.name

    try:
        projects = import_projects_from_csv(temp_path)

        st.success(f"✅ Imported {len(projects)} projects!")
        
        # Preview projects
        for project in projects:
            with st.expander(f"{project.name} ({project.status})"):
                st.markdown(f"**Summary:** {project.summary}")
                st.markdown(f"**Type:** {project.type}")
                st.markdown(f"**Stage:** {project.stage}")
                st.markdown(f"**Progress:** {project.progress}%")
                st.markdown(f"**Tags:** {', '.join(project.tags)}")
                st.markdown(f"**GitHub:** {project.githubUrl}")
                st.markdown(f"**Website:** {project.websiteUrl}")
                st.markdown(f"**Next Action:** {project.nextAction}")
                st.markdown(f"**Activity Log:**")
                st.markdown("<br>".join(f"- {a}" for a in project.activityLog), unsafe_allow_html=True)

        # Save to JSON
        if st.button("💾 Save to projects.json"):
            save_projects_to_json(projects, "data/projects.json")
            st.success("Projects saved to data/projects.json!")

    except Exception as e:
        st.error(f"❌ Failed to import: {e}")
