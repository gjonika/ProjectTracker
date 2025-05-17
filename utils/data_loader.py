import pandas as pd
import json
from datetime import datetime

def import_projects_from_csv(uploaded_file, json_path="data/projects.json"):
    # 🔁 Load existing JSON data
    try:
        with open(json_path, "r") as f:
            existing = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing = []

    # ✅ Read uploaded CSV (Streamlit uploads are file-like objects)
    df = pd.read_csv(uploaded_file)

    # 🧠 Convert each row into project JSON format
    new_projects = []
    for _, row in df.iterrows():
        new_projects.append({
            "name": row["name"],
            "summary": row.get("summary", ""),
            "description": row.get("description", ""),
            "type": row.get("type", "personal").lower(),
            "usefulness": int(row.get("usefulness", 3)),
            "status": row.get("status", "idea").lower(),
            "stage": row.get("stage", "idea"),
            "isMonetized": str(row.get("isMonetized", "false")).lower() == "true",
            "githubUrl": row.get("githubUrl", ""),
            "websiteUrl": row.get("websiteUrl", ""),
            "nextAction": row.get("nextAction", ""),
            "lastUpdated": row.get("lastUpdated", datetime.today().strftime("%Y-%m-%d")),
            "progress": int(row.get("progress", 0)),
            "activityLog": [s.strip() for s in str(row.get("activityLog", "")).split(";") if s.strip()],
            "tags": [t.strip() for t in str(row.get("tags", "")).split(";") if t.strip()]
        })

    # 💾 Save combined result
    with open(json_path, "w") as f:
        json.dump(existing + new_projects, f, indent=2)

    return len(new_projects)
