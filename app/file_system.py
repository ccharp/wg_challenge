import subprocess
from pathlib import Path
from typing import List


def concat_paths(p1: str, p2: str) -> Path:
    return Path(p1) / Path(p2)

def validate_path(path: Path) -> bool:
    # TODO: I'm sure there are security issues I've missed. We'd want to be
    #       VERY careful access to (at least) the local file system. 
    return path.exists()

def build_file_info(path: Path) -> dict:
    return {
        "filename": path.name,
        "owner": path.owner(),
        "group": path.group(),
        "size": path.stat().st_size,
        "permissions": oct(path.stat().st_mode),
    }

def ls_dir(path: Path) -> List[dict]:
    glob = path.glob("*")
    return [build_file_info(p) for p in glob]

def ls_file(path: Path) -> List[dict]:
    file_info = build_file_info(path)
    file_info['file_contents'] = path.read_text()
    return file_info

# TODO: what exceptions can come up from this?
def ls(path: Path) -> str:
    if path.is_file():
        return ls_file(path)

    return ls_dir(path)

# TODO: I'm not comfortable enough with security considerations here 
#       but here's the idea...
def rmdir(path: Path) -> bool:
    return path.unlink()

# # TODO: what exceptions can come up from this?
# def mkdir(path: str) -> bool:
#     return subprocess.check_output(['mkdir', path])
# 
# # TODO: what exceptions can come up from this?
# def touch(path: str) -> bool:
#     return subprocess.check_output(['touch', path])
