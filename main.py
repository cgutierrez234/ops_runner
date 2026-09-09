from job import Job
from executor import Executor
from job_queue import JobQueue

if __name__ == "__main__":

    job = Job("succeeding-job", "true")
    job2 = Job("failing-job", "false")
    job3 = Job("really-failing-job", "this_is_bogus")

    job_queue = JobQueue()

    job_queue.add_job(job)
    job_queue.add_job(job2)
    job_queue.add_job(job3)
    

    my_exec = Executor()

    while job_queue.has_jobs():
        job_to_do = job_queue.pop_job()
        my_result = my_exec.run_job(job_to_do)
        print(my_result)
       

   