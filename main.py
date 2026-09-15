from executor import Executor
from job_queue import JobQueue
from pathlib import Path
from cleanup import run_cleanup
from job_loader import load_jobs

if __name__ == "__main__":
    # Set home directory
    home = Path.home()

# Load the jobs from the JSON config. This gives the program its spine
    json_to_load = home / "Desktop" / "ops_runner"/ "jobs.json"
    jobs = load_jobs(json_to_load)
    
    job_queue = JobQueue()

    for job in jobs:

        job_queue.add_job(job)
    
    my_exec = Executor()

    while job_queue.has_jobs():
        job_to_do = job_queue.pop_job()
        my_result = my_exec.run_job(job_to_do)
        print(my_result)

# Create a path for cleaning up a certain directory
    
    downloads = home / "Downloads"
    run_cleanup(downloads,30)

    

    
    