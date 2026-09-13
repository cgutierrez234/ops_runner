from pathlib import Path
from datetime import datetime, timedelta

def find_cleanup_candidates(directory: Path, days: int) -> list[Path]:

    files_to_consider = []
    cutoff_time = datetime.now() - timedelta(days=days)

    for file in directory.glob("*"):

        modified_time = datetime.fromtimestamp(file.stat().st_mtime)

        if file.is_file():

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

def delete_selected_file(file: Path):

    confirm_delete = input(f"Are you sure you want to delete: {file}? ")

    valid_responses = ['y', 'n']

    while  confirm_delete.lower() not in valid_responses:
        confirm_delete = input("Invalid response. Enter y or n: ")

    if confirm_delete.lower() == 'y':
        confirm_delete_again = input(f"ARE YOU ABSOLUTELY SURE YOU WANT TO DELETE {file} ?!?!?!?!")
        if confirm_delete_again.lower() == 'y':
            print(f"Deleting {file} . . . ")
            file.unlink()
        






