from dataclasses import dataclass
from pathlib import Path

@dataclass
class CleanupConfig:
    directory : Path
    days: int