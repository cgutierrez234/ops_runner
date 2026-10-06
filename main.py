from jobs.executor import Executor
from jobs.job_queue import JobQueue
from pathlib import Path
from cleanup.cleanup import run_cleanup
from loader import load_jobs, load_cleanup_configs
from cli import clear_screen, display_main_menu,  select_cleanup_config, select_job, choose_cleanup_mode, choose_hist_to_display, display_history, display_disk_health, display_backup_result, choose_dir_to_backup, display_largest_file
from history import job_result_to_dict, write_history_file, read_history, filter_recent_history
from backup import directory_discovery
from jobs.job import JobStatus
from cli_commanding import parse_cli_args, run_cli_job
from interactive_mode import run_interactive

if __name__ == "__main__":
    # Set home directory
    home = Path.home()

    # cli args setup
    cli_args = parse_cli_args()

# Load the jobs from their JSON config. Happens at intiation of ops-runner. Objects are waiting in memory
    jobs_json_to_load = home / "Desktop" / "ops_runner"/ "jobs.json"
    jobs = load_jobs(jobs_json_to_load)

    # Load the cleanup_config from its JSON file. Happens at intiation of ops-runner. Objects are waiting in memory
    cleanup_config_to_load = home / "Desktop" / "ops_runner" / "cleanup.json"
    cleanup_configs = load_cleanup_configs(cleanup_config_to_load)

    if cli_args.mode == "interactive":
        run_interactive(jobs, cleanup_configs)
    elif cli_args.mode == "run":
        run_cli_job(jobs, cli_args.job_name, home / "Desktop" / "ops_runner" / "job_history.jsonl")

   
            

    





 

    







    

    
    
