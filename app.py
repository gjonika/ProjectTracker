import streamlit as st

st.set_page_config(page_title="My Projects", layout="centered")

# Demo data
projects = [
    {
        "name": "Project Dashboard",
        "description": "Track all side projects in one place",
        "status": "🚧 In Progress",
        "stage": "🔧 Build",
        "type": "Personal",
        "progress": 75,
        "tags": ["React", "Personal"],
    },
    {
        "name": "Recipe Manager",
        "description": "Simple recipe organizer app",
        "status": "✅ Live",
        "stage": "📈 Market",
        "type": "For Sale",
        "progress": 100,
        "tags": ["Food", "Commercial"],
    }
]

st.title("📋 My Project Tracker")

for p in projects:
    with st.container():
        st.subheader(f"{p['name']} {p['status']}")
        st.caption(p["description"])
        st.progress(p["progress"] / 100)
        st.text(f"Stage: {p['stage']} | Type: {p['type']}")
        st.text("Tags: " + ", ".join(p["tags"]))
        st.divider()
