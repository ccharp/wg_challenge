import os
import subprocess
from typing import List
from pathlib import Path

def concat_paths(p1: str, p2: str) -> Path:
    return Path(p1) / Path(p2)

def validate_path(path: Path) -> bool:
    # TODO: I'm sure there are security issues I've missed. We'd want to be
    #       VERY careful access to (at least) the local file system. 
    return path.exists()

# TODO: what exceptions can come up from this?
# TODO: assumptions
def ls(path: Path) -> str:
    # TODO: does split lines work if there are no files?
    glob = path.glob("*")

    build_obj = lambda p : {
            "filename": p.name,
            "owner": p.owner(),
            "group": p.group(),
            "size": p.stat().st_size,
            "permissions": oct(p.stat().st_mode),
    }

    return [build_obj(p) for p in glob]

# TODO: I'm not comfortable enough with security considerations here 
def rmdir(path: Path) -> bool:
    return path.unlink()

# TODO: what exceptions can come up from this?
# TODO: assumptions
def mkdir(path: str) -> bool:
    return subprocess.check_output(['mkdir', path])

# TODO: what exceptions can come up from this?
# TODO: assumptions
def touch(path: str) -> bool:
    return subprocess.check_output(['touch', path])
