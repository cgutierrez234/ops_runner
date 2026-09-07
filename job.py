from dataclasses import dataclass
from job_status import JobStatus


@dataclass
class Job:
    job_name: str
    job_command: str
    status: JobStatus = JobStatus.QUEUED




  
job = Job("backup-config", "cp config.json backup/config.json")
print(job)