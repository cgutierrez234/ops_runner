from datetime import datetime, timedelta
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
    job_result_dict["Job_Name"] = job_result.job.job_name
    job_result_dict["Job_Command"] = job_result.job.job_command
    job_result_dict["Timeout"] = job_result.job.timeout
    job_result_dict["Status"] = str(job_result.status)
    job_result_dict["Return_Code"] = job_result.return_code
    job_result_dict["Std_out"] = job_result.stdout
    job_result_dict["Std_err"] = job_result.stderr
    job_result_dict["Py_Func_Result"] = job_result.py_func_result

    return job_result_dict

def read_history(hist_file: Path):

    try:
        with open(hist_file, "r") as file:
            for line in file:
                record = json.loads(line)
                yield record
    except FileNotFoundError:
        print(f"{hist_file.name} does not exist")

def filter_recent_history(records): # <--- records is a generator that yields dictionaries. 

    for record in records:
        time_stamp = record["Time_Written"]
        converted_time_stamp = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
        curr_time = datetime.now()
        one_week_ago = curr_time - timedelta(weeks=1) 

        if converted_time_stamp >= one_week_ago:
            yield record
    
