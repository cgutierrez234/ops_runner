from collections import deque
from job import Job


class JobQueue:
    def __init__(self):
        self.my_deque = deque()


    def add_job(self, job: Job):
        self.my_deque.append(job)

    def pop_job(self) -> Job:
        return self.my_deque.popleft()

    def has_jobs(self) -> bool:
        return bool(self.my_deque)