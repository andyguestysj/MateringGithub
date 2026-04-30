from typing import Any, Dict, List
from ..data.json_store import JsonStore
from ..utils.input_helpers import ask_int, ask_text, pause

class CrudMenu:
    def __init__(self, title: str, store: JsonStore, fields: List[str]):
        self.title = title
        self.store = store
        self.fields = fields

    def run(self) -> None:
        while True:
            print(f"\n{self.title}")
            print("1. List entries")
            print("2. View entry")
            print("3. Add entry")
            print("4. Edit entry")
            print("5. Delete entry")
            print("6. Back")
            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.list_entries()
            elif choice == "2":
                self.view_entry()
            elif choice == "3":
                self.add_entry()
            elif choice == "4":
                self.edit_entry()
            elif choice == "5":
                self.delete_entry()
            elif choice == "6":
                return
            else:
                print("Unknown option.")

    def list_entries(self) -> None:
        entries = self.store.load_all()
        if not entries:
            print("No entries found.")
            pause()
            return
        for entry in entries:
            print(f'{entry.get("id")}: {entry.get("name", "Unnamed")}')
        pause()

    def view_entry(self) -> None:
        entry = self.store.find_by_id(ask_int("Entry id"))
        if entry is None:
            print("Entry not found.")
        else:
            print()
            for key, value in entry.items():
                print(f"{key}: {value}")
        pause()

    def add_entry(self) -> None:
        created = self.store.add(self.ask_for_entry())
        print(f'Added entry with id {created["id"]}.')
        pause()

    def edit_entry(self) -> None:
        entry_id = ask_int("Entry id")
        existing = self.store.find_by_id(entry_id)
        if existing is None:
            print("Entry not found.")
            pause()
            return
        updated = self.ask_for_entry(existing)
        print("Entry updated." if self.store.update(entry_id, updated) else "Entry could not be updated.")
        pause()

    def delete_entry(self) -> None:
        entry_id = ask_int("Entry id")
        confirm = input("Delete this entry? Type yes to confirm: ").strip().lower()
        if confirm != "yes":
            print("Delete cancelled.")
            pause()
            return
        print("Entry deleted." if self.store.delete(entry_id) else "Entry not found.")
        pause()

    def ask_for_entry(self, existing: Dict[str, Any] | None = None) -> Dict[str, Any]:
        existing = existing or {}
        entry: Dict[str, Any] = {}
        for field in self.fields:
            label = field.replace("_", " ").title()
            default = str(existing.get(field, "")) or None
            entry[field] = ask_text(label, default)
        return entry
