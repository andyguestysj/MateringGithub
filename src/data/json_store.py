import json
from pathlib import Path
from typing import Any, Dict, List, Optional

class JsonStore:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load_all(self) -> List[Dict[str, Any]]:
        if not self.file_path.exists():
            return []
        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError(f"Expected a list in {self.file_path}")
        return data

    def save_all(self, entries: List[Dict[str, Any]]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(entries, file, indent=4)
            file.write("\n")

    def get_next_id(self) -> int:
        entries = self.load_all()
        if not entries:
            return 1
        return max(int(entry.get("id", 0)) for entry in entries) + 1

    def find_by_id(self, entry_id: int) -> Optional[Dict[str, Any]]:
        for entry in self.load_all():
            if int(entry.get("id", -1)) == entry_id:
                return entry
        return None

    def add(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        entries = self.load_all()
        entry["id"] = self.get_next_id()
        entries.append(entry)
        self.save_all(entries)
        return entry

    def update(self, entry_id: int, updated_entry: Dict[str, Any]) -> bool:
        entries = self.load_all()
        for index, entry in enumerate(entries):
            if int(entry.get("id", -1)) == entry_id:
                updated_entry["id"] = entry_id
                entries[index] = updated_entry
                self.save_all(entries)
                return True
        return False

    def delete(self, entry_id: int) -> bool:
        entries = self.load_all()
        new_entries = [entry for entry in entries if int(entry.get("id", -1)) != entry_id]
        if len(new_entries) == len(entries):
            return False
        self.save_all(new_entries)
        return True
