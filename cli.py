from cleanup_config import CleanupConfig
from job import Job

import os

def display_main_menu() -> int:
    menu_options = ["Run Jobs", "Run Cleanup", "Exit"]
    
    for index, option in enumerate(menu_options):
        print(f"{index + 1}. {option}")
    
    while True:

        startup_choice = input("Please make your selection: ")

        try:
            startup_choice = int(startup_choice)
            if startup_choice < 1 or startup_choice > len(menu_options):
                print(f"Your selection needs to to be from the list of options")
                continue
            else:
                break
        except ValueError:
            continue

    return startup_choice


def select_cleanup_config(cleanup_configs: list[CleanupConfig]) ->CleanupConfig:

    # iterate loaded cleanup_configs and create a nice little cutesy menu
    for index, config in enumerate(cleanup_configs):
        print(f"{index + 1}. {config}")

    while True: 

        user_choice = input("Please select your cleanup option(a numeric option you've been provided): ")

        try:
            user_choice = int(user_choice)
            if user_choice < 1 or user_choice > len(cleanup_configs):
                print(f"Your selection needs to to be from the list of options")
                continue
            else:
                break
        except ValueError:
            continue

    user_choice = user_choice - 1

    return cleanup_configs[user_choice]

def select_job(jobs: list[Job]) -> Job:

    for index, job in enumerate(jobs):
        print(f"{index + 1}. {job}")

    while True: 
        user_choice = input("Please select the Job you want to perform(a numeric option you've been provided)")

        try:
            user_choice = int(user_choice)
            if user_choice < 1 or user_choice > len(jobs):
                print(f"Your selection needs to to be from the list of options")
                continue
            else:
                break
        except ValueError:
            continue
    user_choice = user_choice - 1

    return jobs[user_choice]

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        print("\033[3J", end="")

    