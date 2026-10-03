import json
import sys

from jobs.job import Job
from pathlib import Path
from cleanup.cleanup_config import CleanupConfig
from job_registry import job_functions



def load_jobs(file_name: Path) -> list[Job]:

    loaded_jobs = []
    try:
        with open(file_name, "r") as file:
            jobs =  json.load(file)
    except FileNotFoundError:
        print("jobs.json not found")
        sys.exit(1) # <--- end the python program right now.
    except json.JSONDecodeError:
        print("jobs.json config file is malformed.")
        sys.exit(1)

    for job in jobs:
        try:
            name = job["job_name"]
            if not isinstance(name, str):
                print(f"Job '{name}' has an invalid name: {name!r}")
                continue

            args = tuple(job.get("args", [])) ## args is the key to retrieve, the empty list [] is the default when it is missing. Not all jobs have them in ops runner

            if name in job_functions: # < --- here we check if the json job_name is in job_functions dict that holds python functions. 
                job_function = job_functions[name] # <---- if it is extract the function into job_function
                command = None
                timeout = None
            else:
                job_function = None
                command = job["job_command"]

                if not isinstance(command, str):
                    print(f"Job '{name}' has an invalid command: {command!r}")
                    continue

                timeout = job.get("timeout")
                if not isinstance(timeout, int) and timeout is not None:
                    print(f"Job '{name}' has an invalid timeout: {timeout!r}")
                    continue
        except KeyError as error:
                print(error)
                continue
        
        new_job = Job(name, command, job_function, args=args, timeout=timeout)
        loaded_jobs.append(new_job)

    return loaded_jobs

def load_cleanup_configs(file_name: Path) -> list[CleanupConfig]:

    loaded_configs = []

    try:
        with open(file_name, "r") as file:
            configs = json.load(file)
    except FileNotFoundError:
        print("cleanup.json not found")
        sys.exit(1)
    except json.JSONDecodeError:
            print("cleanup.json config file is malformed.")
            sys.exit(1)

    for config in configs:

        try:
            directory = Path(config["directory"]).expanduser() # < ---- this expands something like ~/Downalods into a full path
            if not directory.exists():
                print(f"Cleanup directory {directory} does not exist.")
                continue
            days = config["days"]
            if not isinstance(days, int):
                print(f"Days variable is not of type int")
                continue
        except KeyError as error:
            print(error)
            continue
        new_config = CleanupConfig(directory, days)
        loaded_configs.append(new_config)

    return loaded_configs


            
