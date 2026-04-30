from pathlib import Path
from .data.campaign_loader import CampaignLoader
from .menus.main_menu import MainMenu

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CAMPAIGNS_DIR = PROJECT_ROOT / "campaigns"

def run_app() -> None:
    loader = CampaignLoader(CAMPAIGNS_DIR)
    campaign_name = loader.get_default_campaign_name()
    if campaign_name is None:
        print("No campaigns found. Create a folder inside campaigns/ first.")
        return
    MainMenu(loader, campaign_name).run()
