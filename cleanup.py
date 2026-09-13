from pathlib import Path
from datetime import datetime, timedelta

def find_cleanup_candidates(directory: Path, days: int) -> list[Path]:

    files_to_consider = []
    cutoff_time = datetime.now() - timedelta(days=days)

    for file in directory.glob("*"):

        modified_time = datetime.fromtimestamp(file.stat().st_mtime)

        if modified_time < cutoff_time:
            files_to_consider.append(file)

    return files_to_consider

def reporter(files: list[Path]) -> dict: 

    file_age_dict = {}
    
    for file in files:

        modified_time = datetime.fromtimestamp(file.stat().st_mtime)
        now = datetime.now()
        days_old = now - modified_time
        num_days = days_old.days

        file_age_dict[file] = num_days

    return file_age_dict




