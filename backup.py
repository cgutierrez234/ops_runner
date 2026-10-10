import shutil

from datetime import datetime
from pathlib import Path

def run_backup(selected_path: Path) -> str:
    home = Path.home()
    selected_path = Path(selected_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = home / "backups" / f"{selected_path.name}_backup_{timestamp}"
    shutil.copytree(selected_path, backup_dir )

    return str(backup_dir) # <-- so the history writer can serialize it


def directory_discovery() -> list:
    home_dir = Path.home()
    dirs_of_interest = {"Downloads", "Desktop", "Documents"}
    sub_directories = [x for x in home_dir.iterdir() if x.is_dir() and  x.name in dirs_of_interest]

    return sub_directories