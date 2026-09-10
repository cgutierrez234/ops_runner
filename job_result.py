from dataclasses import dataclass
from job import Job
from job_status import JobStatus

@dataclass
class JobResult:
    job: Job
    status: JobStatus
    return_code: int | None
    stdout: str | None
    stderr: str | None