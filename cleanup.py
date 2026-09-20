from pathlib import Path
from cleanup_config import CleanupConfig
from datetime import datetime, timedelta
from cli import clear_screen

import json

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

def delete_selected_file(file: Path) -> int:

    confirm_delete = input(f"Are you sure you want to delete: {file}? ")

    valid_responses = ['y', 'n']

    while  confirm_delete.lower() not in valid_responses:
        confirm_delete = input("Invalid response. Enter y or n: ")

    if confirm_delete.lower() == 'y':
        confirm_delete_again = input(f"ARE YOU ABSOLUTELY SURE YOU WANT TO DELETE {file} ?!?!?!?!")
        if confirm_delete_again.lower() == 'y':
            print(f"Deleting {file} . . . ")
            file.unlink()
            return 1 
    return 0

def delete_all_files(files: list[Path]) -> int:

    deleted_files = 0

    for file in files:
        print(f"File: {file}")

    confirm_delete_all = input("Are you sure you want to delete the above files? ")

    valid_responses = ['y', 'n']

    while confirm_delete_all.lower() not in valid_responses:
        confirm_delete_all = input("Invalid response. Enter y or n: ")

    if confirm_delete_all.lower() == 'y':
        confirm_delete_all_again = input(f"ARE YOU ABSOLUTELY SURE YOU WANT TO DELETE ALL FILES?!?!?!?!?!")
        if confirm_delete_all_again.lower() == 'y':
            print(f"Deleting all files . . .")
            for file in files:
                file.unlink()
                deleted_files += 1
        else: 
            clear_screen()
            return 0
    else:
        clear_screen()
        return 0

    return deleted_files

def run_cleanup(config: CleanupConfig, mode: int):

    num_deleted_files = 0

    files_to_delete = find_cleanup_candidates(config.directory, config.days)

    if not files_to_delete:
            print("There are no files for cleanup")
            return
    
    my_report = reporter(files_to_delete)

    if mode == 1:

        for file, age in my_report.items():
            print(f"File '{file.name}' is {age} days old")
        
    
    if mode == 2:

        num_deleted_files = delete_all_files(files_to_delete)

    if mode == 3:
        for index, file in enumerate(files_to_delete):
            print(f"{index + 1}. {file.name}")

        while True: 
            user_choice = input("Please select the file you want to delete(a numeric option you've been provided)")
    
            try:
                user_choice = int(user_choice)
                if user_choice < 1 or user_choice > len(files_to_delete):
                    print(f"Your selection needs to to be from the list of options")
                    continue
                else:
                    break
            except ValueError:
                continue
        
        user_choice = user_choice - 1
        num_deleted_files = delete_selected_file(files_to_delete[user_choice])

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result = {}

    result["Time_Written"] = current_time
    result["Directory"] = str(config.directory)
    result["Mode"] = mode
    result["Candidates_to_delete"]= len(files_to_delete)
    result["Num_Deleted_Files"] = num_deleted_files

    return result

def write_history_file(result: dict):


    with open("cleanup_history", "a") as file:
        json.dump(result, file, indent=4)


        
            
        
   
        






