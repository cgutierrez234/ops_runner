from dataclasses import dataclass
from jobs.job_status import JobStatus
from collections.abc import Callable
from typing import Any


@dataclass
class Job:
    job_name: str
    job_command: str
    job_function: Callable | None = None # <--- is none because existing subprocesses don't have a Python function.
    args: tuple[Any, ...] = ()  # Positional inputs for job_function; defaults to no arguments.
    status: JobStatus = JobStatus.QUEUED
    timeout: int | None = None
    py_func_result: Any | None = None




  
