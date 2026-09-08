from job import Job
from job_status import JobStatus

import subprocess


class Executor:

    #instance method
    def run_job(self, todo_job: Job) -> JobStatus:

        todo_job.status = JobStatus.RUNNING

        result =subprocess.run(todo_job.job_command.split(), capture_output=True, text=True)
        if result.returncode == 0:
            todo_job.status=JobStatus.SUCCESS
        else :
            todo_job.status = JobStatus.FAILED

        return todo_job.status
