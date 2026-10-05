from jobs.executor import Executor
from jobs.job_queue import JobQueue
from pathlib import Path
from cleanup.cleanup import run_cleanup
from loader import load_jobs, load_cleanup_configs
from cli import clear_screen, display_main_menu,  select_cleanup_config, select_job, choose_cleanup_mode, choose_hist_to_display, display_history, display_disk_health, display_backup_result, choose_dir_to_backup, display_largest_file
from history import job_result_to_dict, write_history_file, read_history, filter_recent_history
from backup import directory_discovery
from jobs.job import JobStatus
from cli_commanding import parse_cli_args

if __name__ == "__main__":
    # Set home directory
    home = Path.home()

    # cli args setup
    cli_args = parse_cli_args()

# Load the jobs from their JSON config. Happens at intiation of ops-runner. Objects are waiting in memory
    jobs_json_to_load = home / "Desktop" / "ops_runner"/ "jobs.json"
    jobs = load_jobs(jobs_json_to_load)

    requested_job = None

    for job in jobs:
        if job.job_name == cli_args.job_name:
            requested_job = job 
            break

    if requested_job is None:
        print(f"Unknown job: {cli_args.job_name}")
        raise SystemExit(1)

    if requested_job.job_name in ("backup_dir", "largest_file") and not requested_job.args:
        print(f"Job '{requested_job.job_name}' needs a source direcctory in its JSON args")
        raise SystemExit(1)

    if requested_job.job_name == "largest_file":
        requested_job.args = (Path(requested_job.args[0]),)

    executor = Executor()
    result = executor.run_job(requested_job)

    if requested_job.job_name == "largest_file" and result.py_func_result is not None:
        result.py_func_result = str(result.py_func_result)

    result_record = job_result_to_dict(result)
    write_history_file(result_record, home / "Desktop" / "ops_runner" / "job_history.jsonl")

    if result.status == JobStatus.FAILED:
        print(result.stderr or "Job failed without an error message")
        raise SystemExit(1)

    raise SystemExit(0)

    # Load the cleanup_config from its JSON file. Happens at intiation of ops-runner. Objects are waiting in memory
    cleanup_config_to_load = home / "Desktop" / "ops_runner" / "cleanup.json"
    cleanup_configs = load_cleanup_configs(cleanup_config_to_load)

    while True:

        startup_choice = display_main_menu()
        match startup_choice:
            case 1:

                clear_screen()
                selected_job = select_job(jobs)

                if selected_job is None:
                    clear_screen()
                    continue

                if selected_job.job_name == "backup_dir" or selected_job.job_name == "largest_file":
                    clear_screen()
                    discovered_directories = directory_discovery()
                    dir_to_backup = choose_dir_to_backup(discovered_directories)
                    

                    if dir_to_backup is None:
                        clear_screen()
                        continue

                    selected_job.args = (dir_to_backup,)


                job_queue = JobQueue()
                job_queue.add_job(selected_job)
                
                my_exec = Executor()

                while job_queue.has_jobs():
                    job_to_do = job_queue.pop_job()
                    my_result = my_exec.run_job(job_to_do)
                    clear_screen()

                    if my_result.status == JobStatus.FAILED:
                        print(my_result.stderr or "Job failed without an error message")

                    elif my_result.job.job_name == "largest_file" and my_result.py_func_result is None:
                        print("No files found in the selected directory.")

                    if my_result.py_func_result is not None:    

                        if my_result.job.job_name == "disk_health":
                            display_disk_health(my_result.py_func_result)

                        if my_result.job.job_name == "backup_dir":
                            display_backup_result(my_result.py_func_result)

                        if my_result.job.job_name == "largest_file":
                            display_largest_file(my_result.py_func_result)
                            my_result.py_func_result = str(my_result.py_func_result)
                        
                    my_result_dict = job_result_to_dict(my_result)
                    write_history_file(my_result_dict, Path("job_history.jsonl"))
                    input("Press Enter to return to the main menu . . . ")

                clear_screen()
                

            case 2:

                clear_screen()
                selected_mode = choose_cleanup_mode()
                if selected_mode == 4:
                    clear_screen()
                    continue

                clear_screen()
                config_to_run = select_cleanup_config(cleanup_configs)
                clear_screen()

                result = run_cleanup(config_to_run, selected_mode)
                write_history_file(result, Path("cleanup_history.jsonl"))

            case 3:

                clear_screen()
                selected_hist_choice = choose_hist_to_display()
                if selected_hist_choice == 3:
                    clear_screen()
                    continue

                match selected_hist_choice:

                    case 1:
                        hist_path = Path("job_history.jsonl")
                        job_history = read_history(hist_path)
                        jobs_to_view = filter_recent_history(job_history)

                        for job in jobs_to_view:
                            display_history(job)
                        input("Press Enter to return to the main menu . . . ")
                        clear_screen()

                    case 2:

                        hist_path = Path("cleanup_history.jsonl")
                        cleanup_history = read_history(hist_path)
                        cleanup_to_view = filter_recent_history(cleanup_history)

                        for cleanup in cleanup_to_view:
                            display_history(cleanup)

            case 4:
                clear_screen()
                break
            

    





 

    







    

    
    
