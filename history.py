from datetime import datetime
from pathlib import Path
from jobs.executor import JobResult
import json




def write_history_file(result: dict, history_file: Path):

    with open(history_file, "a") as file:
        json.dump(result, file)
        file.write("\n")


def job_result_to_dict(job_result: JobResult) -> dict:

    job_result_dict = {}
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    job_result_dict["Time_Written"] = current_time
    job_result_dict["Job"] = str(job_result.job)
    job_result_dict["Status"] = str(job_result.status)
    job_result_dict["Return_Code"] = job_result.return_code
    job_result_dict["Std_out"] = job_result.stdout
    job_result_dict["Std_err"] = job_result.stderr

    return job_result_dict