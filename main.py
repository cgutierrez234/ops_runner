from executor import Executor
from job_queue import JobQueue
from pathlib import Path
from cleanup import run_cleanup
from loader import load_jobs, load_cleanup_configs
from cli import select_cleanup_config

if __name__ == "__main__":
    # Set home directory
    home = Path.home()

# Load the jobs from their JSON config. 
    jobs_json_to_load = home / "Desktop" / "ops_runner"/ "jobs.json"
    jobs = load_jobs(jobs_json_to_load)

    # Load the cleanup_config from its JSON file. 
    cleanup_config_to_load = home / "Desktop" / "ops_runner" / "cleanup.json"
    cleanup_configs = load_cleanup_configs(cleanup_config_to_load)

    job_queue = JobQueue()

    for job in jobs:

        job_queue.add_job(job)
    
    my_exec = Executor()

    while job_queue.has_jobs():
        job_to_do = job_queue.pop_job()
        my_result = my_exec.run_job(job_to_do)
        print(my_result)


config_to_run = select_cleanup_config(cleanup_configs)
run_cleanup(config_to_run)

    







    

    
    