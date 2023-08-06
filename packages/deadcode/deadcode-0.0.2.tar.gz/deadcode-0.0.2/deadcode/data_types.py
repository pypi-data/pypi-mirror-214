from dataclasses import dataclass
from typing import List, Optional


FileContent = str
Filename = str  # Contains full path to existing file
Pathname = str  # Can contain wildewards
VariableName = str


@dataclass
class Args:
    paths: List[Pathname]
    exclude: List[Pathname]
    ignore_names: List[Pathname]
    ignore_files: List[Pathname]
