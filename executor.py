from job import Job
from job_status import JobStatus
from job_result import JobResult

import subprocess


class Executor:

    #instance method
    def run_job(self, todo_job: Job) -> JobResult:

        try:

            result =subprocess.run(todo_job.job_command.split(), capture_output=True, text=True, timeout=todo_job.timeout)

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
        except subprocess.TimeoutExpired:
            todo_job.status = JobStatus.FAILED
            return_code = None
            stdout = None
            stderr = None

        my_result = JobResult(

        job = todo_job,
        status = todo_job.status,
        return_code = return_code,
        stdout = stdout,
        stderr = stderr
        )
        
        return my_result
