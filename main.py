from executor import Executor
from job_queue import JobQueue
from pathlib import Path
from cleanup import run_cleanup
from loader import load_jobs, load_cleanup_configs
from cli import  clear_screen, display_main_menu,  select_cleanup_config, select_job

if __name__ == "__main__":
    # Set home directory
    home = Path.home()

# Load the jobs from their JSON config. Happens at intiation of ops-runner. Objects are waiting in memory
    jobs_json_to_load = home / "Desktop" / "ops_runner"/ "jobs.json"
    jobs = load_jobs(jobs_json_to_load)

    # Load the cleanup_config from its JSON file. Happens at intiation of ops-runner. Objects are waiting in memory
    cleanup_config_to_load = home / "Desktop" / "ops_runner" / "cleanup.json"
    cleanup_configs = load_cleanup_configs(cleanup_config_to_load)

    while True:

        startup_choice = display_main_menu()
        match startup_choice:
            case 1:

                clear_screen()
                selected_job = select_job(jobs)

                job_queue = JobQueue()
                job_queue.add_job(selected_job)
                
                my_exec = Executor()

                while job_queue.has_jobs():
                    job_to_do = job_queue.pop_job()
                    my_result = my_exec.run_job(job_to_do)
                    print(my_result)
            case 2:

                clear_screen()
                config_to_run = select_cleanup_config(cleanup_configs)
                run_cleanup(config_to_run)

            case 3:
                break
            

    





 

    







    

    
    