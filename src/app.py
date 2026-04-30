from pathlib import Path

from .data.campaign_loader import CampaignLoader
from .gui.main_window import run_gui

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CAMPAIGNS_DIR = PROJECT_ROOT / "campaigns"


def run_app() -> None:
    """Create the campaign loader and start the GUI."""
    print("Starting TTRPG Campaign Manager...")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Campaigns directory: {CAMPAIGNS_DIR}")

    if not CAMPAIGNS_DIR.exists():
        raise FileNotFoundError(f"Could not find campaigns folder: {CAMPAIGNS_DIR}")

    loader = CampaignLoader(CAMPAIGNS_DIR)
    run_gui(loader)
