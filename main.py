from job import Job
from executor import Executor
from job_queue import JobQueue

import json
import sys

if __name__ == "__main__":


    job_queue = JobQueue()

    try:

        with open("jobs.json", "r") as file:
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
        
        new_job = Job(name, command, timeout)
        job_queue.add_job(new_job)
    
    my_exec = Executor()

    while job_queue.has_jobs():
        job_to_do = job_queue.pop_job()
        my_result = my_exec.run_job(job_to_do)
        print(my_result)
       

   