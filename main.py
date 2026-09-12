from job import Job
from executor import Executor
from job_queue import JobQueue

import json

if __name__ == "__main__":


    job_queue = JobQueue()

    with open("jobs.json", "r") as file:
       jobs =  json.load(file)

       for job in jobs:
           name = job["job_name"]
           command = job["job_command"]
           timeout = job["timeout"]
           new_job = Job(name, command, timeout)
           job_queue.add_job(new_job)
    
    my_exec = Executor()

    while job_queue.has_jobs():
        job_to_do = job_queue.pop_job()
        my_result = my_exec.run_job(job_to_do)
        print(my_result)
       

   