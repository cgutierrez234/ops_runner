# ops_runner
A Python job orchestration system for scheduling, executing, and tracking operational tasks.

## Interactive mode

Interactive mode provides menus for running jobs, cleaning up files, and viewing history. From the project directory, run:

```bash
python3 main.py interactive
```

Choose an operation from the main menu, then follow its prompts.

## Unattended mode

Unattended mode runs a configured job without menus or prompts. It can be invoked manually or by a scheduler such as cron. From the project directory, run:

```bash
python3 main.py run disk_health
```

The command selects an entry by its `job_name` in `jobs.json`. Python function inputs come from that entry's `args` list, not from additional command-line arguments. Jobs that require a source directory must have it configured before unattended execution.

Execution results are recorded in `job_history.jsonl`. The process exits with code `0` on success or `1` on job failure. Successful unattended execution currently produces no terminal output.

## Current environment

OpsRunner is currently configured for macOS with the repository at `~/Desktop/ops_runner`. Configuration loading and unattended history writing use that location explicitly. Interactive history paths are relative to the working directory, so launch interactive mode from the project directory.

Backups are full directory copies stored in `~/backups/<source-name>_backup_<timestamp>`. They remain on the same disk as the source; they do not protect against disk loss. Backup retention is not currently automated.

## Scheduling with cron

First verify the unattended command manually. Find your Python interpreter with:

```bash
command -v python3
```

Use absolute paths for both Python and `main.py`. The following examples use the interpreter and project location tested during development; replace them with your own paths.

Edit your user schedule with `crontab -e`. Each entry contains five time fields followed by a command:

```text
minute hour day-of-month month day-of-week command
```

An asterisk matches any value in its field. These example entries run disk health daily at 23:59 and backup daily at 23:00:

```cron
59 23 * * * /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 /Users/carlgutierrez/Desktop/ops_runner/main.py run disk_health >> /Users/carlgutierrez/opsrunner-cron.log 2>&1
0 23 * * * /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 /Users/carlgutierrez/Desktop/ops_runner/main.py run backup_dir >> /Users/carlgutierrez/opsrunner-cron.log 2>&1
```

Configure the backup source in the `backup_dir` entry before scheduling it:

```json
{
    "job_name": "backup_dir",
    "args": ["/absolute/path/to/source"]
}
```

Saving the crontab installs the schedule. In Vim, use `:wq`, then confirm the saved entries with:

```bash
crontab -l
```

For a first test, schedule a run a few minutes ahead while the Mac is awake. Verify a new history record and, for backup, a new destination containing the source files. Restore the intended schedule afterward.

Cron does not run missed jobs when the Mac wakes from system sleep. Locking the screen does not itself put the system to sleep, but power settings may do so later. See [Apple's scheduling documentation](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/ScheduledJobs.html).

## Logs, permissions, and troubleshooting

The cron suffix `>> logfile 2>&1` appends both standard output and standard error to one file. This captures startup errors that occur before OpsRunner writes job history. An empty scheduler log can be normal for a successful run.

- **No scheduled result:** check `crontab -l`, confirm the Mac was awake, and inspect `~/opsrunner-cron.log`. Run the exact command manually using its absolute paths.
- **Unknown job:** the command's job name must match a loaded entry in `jobs.json`.
- **Missing source arguments:** configure an `args` list for unattended backup or largest-file jobs. CLI mode never opens directory selection.
- **Permission prompt:** macOS protects Desktop, Documents, and Downloads. Establish the necessary permission before relying on unattended runs, then verify a repeat scheduled run without a prompt. Review access in System Settings → Privacy & Security → Files & Folders. See [Apple's file-access guidance](https://support.apple.com/guide/mac-help/control-access-to-files-and-folders-on-mac-mchld5a35146/mac).
- **Failed backup:** inspect the error in job history or the cron log. A failed copy can leave a partial destination; a destination folder alone does not prove success.

Check the exit status immediately after a manual command with `echo $?`. Successful job execution returns `0`; rejected jobs or failed executions return `1`. Missing or invalid command-line arguments are rejected by `argparse` with exit code `2`.
