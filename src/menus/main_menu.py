from .crud_menu import CrudMenu
from ..data.campaign_loader import CampaignLoader
from ..utils.input_helpers import pause

class MainMenu:
    MENU_CONFIG = {
        "characters": ["name", "class", "level", "description"],
        "locations": ["name", "region", "description"],
        "monsters": ["name", "challenge_rating", "description"],
        "rules": ["name", "category", "description"],
        "adventures": ["name", "status", "description"],
    }

    def __init__(self, loader: CampaignLoader, campaign_name: str):
        self.loader = loader
        self.campaign_name = campaign_name

    def run(self) -> None:
        while True:
            print("\nTTRPG Campaign Manager")
            print(f"Current campaign: {self.campaign_name}")
            print("1. Switch campaign")
            print("2. Manage characters")
            print("3. Manage locations")
            print("4. Manage monsters")
            print("5. Manage rules")
            print("6. Manage adventures")
            print("7. Exit")
            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.switch_campaign()
            elif choice == "2":
                self.open_crud_menu("characters", "Characters")
            elif choice == "3":
                self.open_crud_menu("locations", "Locations")
            elif choice == "4":
                self.open_crud_menu("monsters", "Monsters")
            elif choice == "5":
                self.open_crud_menu("rules", "Rules")
            elif choice == "6":
                self.open_crud_menu("adventures", "Adventures")
            elif choice == "7":
                print("Goodbye.")
                return
            else:
                print("Unknown option.")

    def switch_campaign(self) -> None:
        campaigns = self.loader.list_campaigns()
        if not campaigns:
            print("No campaigns found.")
            pause()
            return
        print("\nAvailable campaigns")
        for index, campaign in enumerate(campaigns, start=1):
            print(f"{index}. {campaign}")
        selected = input("Choose a campaign number: ").strip()
        try:
            self.campaign_name = campaigns[int(selected) - 1]
            print(f"Switched to {self.campaign_name}.")
        except (ValueError, IndexError):
            print("Invalid campaign selection.")
        pause()

    def open_crud_menu(self, data_type: str, title: str) -> None:
        store = self.loader.get_store(self.campaign_name, data_type)
        CrudMenu(title, store, self.MENU_CONFIG[data_type]).run()
