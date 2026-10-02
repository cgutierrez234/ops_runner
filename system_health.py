import shutil

from datetime import datetime
from pathlib import Path


def get_disk_metrics(path: Path) -> dict:

    disk_space_dict = {}

    bytes_in_gb = 1024 ** 3
    total, used, free = shutil.disk_usage(path)

    disk_space_dict["Total_Space"] = round(total / bytes_in_gb, 2)
    disk_space_dict["Used_Space"] = round(used / bytes_in_gb, 2)
    disk_space_dict["Free_Space"] = round(free / bytes_in_gb, 2)
    disk_space_dict["Percentage_Used"] = round((used / total) * 100, 2)
    disk_space_dict["Percentage_Available"] = round((free / total) * 100, 2)

    return disk_space_dict

def check_disk_health(metrics: dict) -> bool:

    total_space = metrics["Total_Space"]
    allowable_threshold = total_space * 0.75

    if metrics["Used_Space"] >= allowable_threshold:
        return False
    else:
        return True

