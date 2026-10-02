from jobs.job import Job
from jobs.job_status import JobStatus
from jobs.job_result import JobResult
from pathlib import Path

import subprocess


class Executor:

    #instance method
    def run_job(self, todo_job: Job) -> JobResult:

        try:
            if todo_job.job_function is not None:

                root_path = Path("/") # <---- get disk metrics takes a path
                py_func_result = todo_job.job_function(root_path) # <---- job_function is registered as 'get_disk_metrics'
                todo_job.status = JobStatus.SUCCESS
                return_code = None
                stdout = None
                stderr = None

            else:
                
                py_func_result = None # <--- with a subprocess job there will be a None result for a python function 

                result = subprocess.run(todo_job.job_command.split(), capture_output=True, text=True, timeout=todo_job.timeout)

                return_code = result.returncode
                stdout = result.stdout
                stderr = result.stderr
                
                if result.returncode == 0:
                    todo_job.status=JobStatus.SUCCESS
                else:
                    todo_job.status=JobStatus.FAILED
        except FileNotFoundError:
            todo_job.status = JobStatus.FAILED
            return_code = None
            stdout = None
            stderr = None
            py_func_result = None
        except subprocess.TimeoutExpired:
            todo_job.status = JobStatus.FAILED
            return_code = None
            stdout = None
            stderr = None
            py_func_result = None

        my_result = JobResult(

        job = todo_job,
        status = todo_job.status,
        return_code = return_code,
        stdout = stdout,
        stderr = stderr,
        py_func_result = py_func_result

        )
        
        return my_result
