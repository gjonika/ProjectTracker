from typing import List, Optional
from datetime import date

class Project:
    def __init__(
        self,
        id: str,
        name: str,
        summary: str,
        description: str,
        type: str,
        usefulness: int,
        status: str,
        stage: str,
        isMonetized: bool,
        githubUrl: Optional[str],
        websiteUrl: Optional[str],
        nextAction: Optional[str],
        lastUpdated: Optional[str],
        progress: int,
        activityLog: List[str],
        tags: List[str],
    ):
        self.id = id
        self.name = name
        self.summary = summary
        self.description = description
        self.type = type
        self.usefulness = usefulness
        self.status = status
        self.stage = stage
        self.isMonetized = isMonetized
        self.githubUrl = githubUrl
        self.websiteUrl = websiteUrl
        self.nextAction = nextAction
        self.lastUpdated = lastUpdated or str(date.today())
        self.progress = progress
        self.activityLog = activityLog
        self.tags = tags
