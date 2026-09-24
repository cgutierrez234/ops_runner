from dataclasses import dataclass
from jobs.job import Job
from jobs.job_status import JobStatus

@dataclass
class JobResult:
    job: Job
    status: JobStatus
    return_code: int | None
    stdout: str | None
    stderr: str | None