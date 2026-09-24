from dataclasses import dataclass
from jobs.job_status import JobStatus


@dataclass
class Job:
    job_name: str
    job_command: str
    status: JobStatus = JobStatus.QUEUED
    timeout: int | None = None




  
