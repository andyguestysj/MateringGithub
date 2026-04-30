from pathlib import Path
from typing import List, Optional
from .file_manager import FileManager
from .json_store import JsonStore

class CampaignLoader:
    DATA_FILES = {
        "characters": "characters.json",
        "locations": "locations.json",
        "monsters": "monsters.json",
        "rules": "rules.json",
        "adventures": "adventures.json",
    }

    def __init__(self, campaigns_dir: Path):
        self.campaigns_dir = campaigns_dir

    def list_campaigns(self) -> List[str]:
        return FileManager.list_folders(self.campaigns_dir)

    def get_default_campaign_name(self) -> Optional[str]:
        campaigns = self.list_campaigns()
        if not campaigns:
            return None
        if "starter_campaign" in campaigns:
            return "starter_campaign"
        return campaigns[0]

    def get_campaign_path(self, campaign_name: str) -> Path:
        return self.campaigns_dir / campaign_name

    def get_store(self, campaign_name: str, data_type: str) -> JsonStore:
        if data_type not in self.DATA_FILES:
            raise ValueError(f"Unknown data type: {data_type}")
        return JsonStore(self.get_campaign_path(campaign_name) / self.DATA_FILES[data_type])
