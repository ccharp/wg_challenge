from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException

from . import config
from . import file_system as fs

app = FastAPI()

# Using lru_cache allows config updates to automatically be picked up. This means we
#   can test multiple configurations (e.g. active_paths) without restarting the server.
@lru_cache()
def get_settings():
    return config.Settings()

def build_response(path: str, output: str):
    return {
        "path": path,
        "output": output
    }

# TODO: can this be combined with path_get()? 
@app.get("/")
async def root_get(settings: config.Settings = Depends(get_settings)):
    ls_output = fs.ls(Path(settings.active_path))
    return build_response(settings.active_path, ls_output)

@app.get("/{input_path:path}", )
async def path_get(input_path: str, settings: config.Settings = Depends(get_settings)):
    """
    Get the contents of the specific directory relative to the active path (see config.py)
    """
    full_path = Path(settings.active_path) / Path(input_path)
    validate_path(full_path)

    # TODO: what exceptions can this throw?
    ls_output = fs.ls(full_path)

    return build_response(full_path, ls_output)


@app.delete("/{input_path:path}")
async def path (input_path: str, settings: config.Settings = Depends(get_settings)):
    """
    Delete the specific file relative to the active path (see config.py)
    """
    full_path = Path(settings.active_path) / Path(input_path)
    validate_path(full_path)

    # TODO: what exceptions can this throw?
    fs.rmdir(full_path)

    return build_response(full_path, "Deleted")

# Wrapper for boilerplate I anticipate if this were fully fleshed out
def validate_path(path: Path):
    if(not fs.validate_path(path)):
        # Right now, this only comes up with the given path does not exist
        raise HTTPException(status_code=404, detail="Invalid path")


# TODO: implement put and post
# @app.put("/{full_path:path}")
# async def path(full_path: str):
#     return {"path": full_path}
#
# @app.post("/{full_path:path}")
# async def path(full_path: str):
#     # To keep things simple, if path ends with /, we make directory
#     if full_path.endswith("/"):
#         fs.mkdir(full_path)
#     else:
#         fs.touch(full_path)
#     return {"path": full_path}

