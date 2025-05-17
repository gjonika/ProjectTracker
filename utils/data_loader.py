import pandas as pd
import json
from datetime import datetime

def safe_int(value, default=0):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

def import_projects_from_csv(uploaded_file, json_path="data/projects.json"):
    # 🔁 Load existing JSON data
    try:
        with open(json_path, "r") as f:
            existing = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing = []

    # ✅ Read uploaded CSV
    df = pd.read_csv(uploaded_file)

    # 🧠 Convert each row into project JSON format
    new_projects = []
    for _, row in df.iterrows():
        new_projects.append({
            "name": str(row.get("name", "")).strip(),
            "summary": str(row.get("summary", "")).strip(),
            "description": str(row.get("description", "")).strip(),
            "type": str(row.get("type", "")).strip(),
            "usefulness": int(row.get("usefulness", 0)),
            "status": str(row.get("status", "")).lower().strip(),
            "stage": str(row.get("stage", "")).strip(),
            "isMonetized": str(row.get("isMonetized", "")).lower() == "true",
            "githubUrl": str(row.get("githubUrl", "")).strip(),
            "websiteUrl": str(row.get("websiteUrl", "")).strip(),
            "nextAction": str(row.get("nextAction", "")).strip(),
            "lastUpdated": str(row.get("lastUpdated", "")).strip(),
            "progress": int(row.get("progress", 0)),
            "activityLog": [x.strip() for x in str(row.get("activityLog", "")).split(";") if x],
            "tags": [x.strip() for x in str(row.get("tags", "")).split(",") if x],
        })

    # 💾 Save combined result
    with open(json_path, "w") as f:
        json.dump(existing + new_projects, f, indent=2)

    return len(new_projects)


def load_projects_from_json(json_path):
    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
