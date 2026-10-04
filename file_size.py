from pathlib import Path


def determine_largest_file(working_dir: Path) -> Path | None:

    if working_dir.exists():

        files = [x for x in working_dir.rglob("*") if x.is_file()]

        if files:
            largest_file = max(files, key=lambda file: file.stat().st_size) # <---- lambda gets the size of every file, then max returns the largest file. 
        else:
            return None
    else:
        raise FileNotFoundError(f"{working_dir} does not exist")

    return largest_file
