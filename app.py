import streamlit as st
from utils.data_loader import (
    import_projects_from_csv,
    save_projects_to_json,
    load_projects_from_json,
)
import os
import tempfile

st.set_page_config(page_title="Project Tracker", layout="wide")

tabs = st.tabs(["📥 Import CSV", "📋 View Projects"])

# === 1. IMPORT TAB ===
with tabs[0]:
    st.title("📥 Import Projects from CSV")

    st.download_button(
        label="📄 Download CSV Template",
        data=open("templates/sample_projects.csv", "rb").read(),
        file_name="sample_projects.csv",
        mime="text/csv",
    )

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded_file.getvalue())
            temp_path = tmp.name

        try:
            projects = import_projects_from_csv(temp_path)

            st.success(f"✅ Imported {len(projects)} projects!")

            for project in projects:
                with st.expander(f"{project.name} ({project.status})"):
                    st.markdown(f"**Summary:** {project.summary}")
                    st.markdown(f"**Type:** {project.type}")
                    st.markdown(f"**Stage:** {project.stage}")
                    st.progress(project.progress / 100)
                    st.markdown(f"**Tags:** {', '.join(project.tags)}")
                    st.markdown(f"**GitHub:** {project.githubUrl}")
                    st.markdown(f"**Website:** {project.websiteUrl}")
                    st.markdown(f"**Next Action:** {project.nextAction}")
                    st.markdown(f"**Activity Log:**")
                    st.markdown("<br>".join(f"- {a}" for a in project.activityLog), unsafe_allow_html=True)

            if st.button("💾 Save to projects.json"):
                save_projects_to_json(projects, "data/projects.json")
                st.success("Projects saved!")

        except Exception as e:
            st.error(f"❌ Failed to import: {e}")


# === 2. VIEW PROJECTS TAB ===
with tabs[1]:
    st.title("📋 Project Dashboard")

    json_path = "data/projects.json"

    if os.path.exists(json_path):
        projects = load_projects_from_json(json_path)

        if not projects:
            st.info("No projects to display yet.")
        else:
            for project in projects:
                with st.container():
                    st.subheader(f"{project.name} {project.status}")
                    st.caption(project.summary)
                    st.progress(project.progress / 100)
                    st.markdown(f"**Stage:** {project.stage} | **Type:** {project.type}")
                    st.markdown(f"**Tags:** {', '.join(project.tags)}")
                    st.markdown(f"**Next Action:** {project.nextAction}")
                    st.markdown(f"[GitHub]({project.githubUrl}) | [Website]({project.websiteUrl})")
                    st.divider()
    else:
        st.warning("⚠️ No projects.json file found. Please import a CSV first.")
