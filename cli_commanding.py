import argparse

from history import job_result_to_dict, write_history_file
from pathlib import Path
from jobs.job import Job,JobStatus
from jobs.executor import Executor

def parse_cli_args():

   # decalre the parser
   parser = argparse.ArgumentParser(description="Run a configured OpsRunner Job") 

   commands = parser.add_subparsers(dest="mode", required=True) # dest="mode" stores the selected command in cli_args.mode/ required=True makes a missing command a usage error
   commands.add_parser("interactive", help="Open the interactive menu") # FOR INTERACTIVE MODE

   run_parser = commands.add_parser("run", help="Run a configured Job") # FOR STRICTLY CLI MODE
   run_parser.add_argument("job_name", help="Name of the configured job to run")

   return parser.parse_args()

def run_cli_job(jobs: list[Job], target_name: str, history_file_path: Path):

   requested_job = None
   
   for job in jobs:
      if job.job_name == target_name:
         requested_job = job 
         break

   if requested_job is None:
      print(f"Unknown job: {target_name}")
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
   write_history_file(result_record, history_file_path)

   if result.status == JobStatus.FAILED:
      print(result.stderr or "Job failed without an error message")
      raise SystemExit(1)

   raise SystemExit(0)