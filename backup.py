import shutil

from datetime import datetime
from pathlib import Path

def run_backup(selected_path: Path) -> str:

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{selected_path}_backup_{timestamp}"
    shutil.copytree(selected_path, backup_dir )

    return backup_dir


def directory_discovery() -> list:
    home_dir = Path.home()
    dirs_of_interest = {"Downloads", "Desktop", "Documents"}
    sub_directories = [x for x in home_dir.iterdir() if x.is_dir() and  x.name in dirs_of_interest]

    return sub_directories