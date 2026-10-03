from system_health import get_disk_metrics
from backup import run_backup

job_functions = {
    "disk_health": get_disk_metrics,
    "backup_dir": run_backup
}