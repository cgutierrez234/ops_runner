from system_health import get_disk_metrics
from backup import run_backup
from file_size import determine_largest_file

job_functions = {
    "disk_health": get_disk_metrics,
    "backup_dir": run_backup,
    "largest_file": determine_largest_file
}