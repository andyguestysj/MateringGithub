from pathlib import Path
from typing import List

class FileManager:
    @staticmethod
    def ensure_folder(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def list_folders(path: Path) -> List[str]:
        if not path.exists():
            return []
        return sorted([item.name for item in path.iterdir() if item.is_dir()])

    @staticmethod
    def file_exists(path: Path) -> bool:
        return path.exists() and path.is_file()
