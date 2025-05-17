import csv
import json
from typing import List
from utils.models import Project


def import_projects_from_csv(file_path: str) -> List[Project]:
    projects = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            project = Project(
                id=row["id"],
                name=row["name"],
                summary=row["summary"],
                description=row["description"],
                type=row["type"],
                usefulness=int(row["usefulness"]),
                status=row["status"],
                stage=row["stage"],
                isMonetized=row["isMonetized"].lower() == "true",
                githubUrl=row.get("githubUrl"),
                websiteUrl=row.get("websiteUrl"),
                nextAction=row.get("nextAction"),
                lastUpdated=row.get("lastUpdated"),
                progress=int(row["progress"]),
                activityLog=[log.strip() for log in row["activityLog"].split(";") if log.strip()],
                tags=[tag.strip() for tag in row["tags"].split(";") if tag.strip()],
            )
            projects.append(project)

    return projects


def save_projects_to_json(projects: List[Project], json_path: str):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([vars(p) for p in projects], f, indent=2, ensure_ascii=False)


def load_projects_from_json(json_path: str) -> List[Project]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Project(**p) for p in data]
