# components/project_dashboard_ui.py

import streamlit as st

def render_project_dashboard_ui(projects=None):
    st.title("📋 Project Dashboard")
    st.caption("Track and manage your side projects")

    # 🔍 Top Filters Row
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
        with col1:
            st.text_input("Search projects...")
        with col2:
            st.selectbox("All Status", ["All", "Idea", "In Progress", "Live", "Abandoned"])
        with col3:
            st.selectbox("All Types", ["All", "Personal", "For Sale"])
        with col4:
            st.selectbox("All Ratings", ["All", "⭐️ 1+", "⭐️ 2+", "⭐️ 3+", "⭐️ 4+", "⭐️ 5"])
        with col5:
            st.checkbox("Show monetized only", value=False)
        with col6:
            st.button("➕ Add Project")

    # 📊 View Controls Row
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            st.button("Show Insights")
        with col2:
            st.button("Import CSV")
        with col3:
            st.radio("View", ["Cards", "Table"], horizontal=True)
        with col4:
            st.button("⬇ JSON")
        with col5:
            st.button("⬇ CSV")

    st.markdown("---")

    # 🔽 Sort Controls
    with st.container():
        sort_cols = st.columns([1, 1, 1, 1])
        with sort_cols[0]:
            st.button("Sort by Name")
        with sort_cols[1]:
            st.button("Sort by Status")
        with sort_cols[2]:
            st.button("Sort by Usefulness")
        with sort_cols[3]:
            st.button("Sort by Progress")

    st.markdown("---")

    # 🧱 Placeholder Cards
    for i in range(3):
        with st.container():
            st.markdown("### Example Project 😎")
            st.markdown("Short summary here")
            st.caption("Longer description")

            col1, col2, col3 = st.columns(3)
            col1.markdown("🚦 **Status:** In Progress")
            col2.markdown("🛠️ **Stage:** Build")
            col3.markdown("🏷️ **Type:** Personal")

            st.progress(0.75)

            st.markdown("⭐ **Usefulness:** 4/5")
            st.markdown("🏷️ **Tags:** Tag1, Tag2")
            st.markdown("🎯 **Next Action:** Research competitors")

            st.markdown("🔗 [GitHub](https://github.com/example) | [Website](https://example.com)")
            st.caption("🕓 Last updated: 2023-05-10")

            with st.expander("📝 Activity Log"):
                st.markdown("- Created the repo")
                st.markdown("- Added login page")

            st.markdown("🗑️ Edit | ❌ Delete")
            st.divider()
