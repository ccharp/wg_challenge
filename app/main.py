from fastapi import FastAPI, HTTPException, Depends

from functools import lru_cache

from . import file_system as fs
from . import config

from pathlib import Path

app = FastAPI()

@lru_cache()
def get_settings():
    return config.Settings()

def build_response(path: str, output: str):
    return {
        "path": path,
        "output": output
    }

# build the full path from active path and input path
# Verify that path is valid by ensure it starts with active path
# perform the operation
@app.get("/")
async def root_get(settings: config.Settings = Depends(get_settings)):
    ls_output = fs.ls(Path(settings.active_path))
    return build_response(settings.active_path, ls_output)

# TODO: can pull path be called "input_path"?
@app.get("/{input_path:path}", )
async def path_get(input_path: str, settings: config.Settings = Depends(get_settings)):
    full_path = Path(settings.active_path) / Path(input_path)
    validate_path(full_path)

    # TODO: what exceptions can this throw?
    ls_output = fs.ls(full_path)

    return build_response(full_path, ls_output)


# TODO: implement
# @app.put("/{full_path:path}")
# async def path(full_path: str):
#     return {"path": full_path}


@app.post("/{full_path:path}")
async def path(full_path: str):
    """

    """
    # To keep things simple, if path ends with /, we make directory
    if full_path.endswith("/"):
        fs.mkdir(full_path)
    else:
        fs.touch(full_path)
    
    return {"path": full_path}


# Only delete files
@app.delete("/{input_path:path}")
async def path (input_path: str, settings: config.Settings = Depends(get_settings)):
    full_path = Path(settings.active_path) / Path(input_path)
    validate_path(full_path)

    # TODO: what exceptions can this throw?
    fs.rmdir(full_path)

    return build_response(full_path, "Deleted")

# Wrapper for boilerplate I anticipate if this were fully fleshed out
def validate_path(path: Path):
    if(not fs.validate_path(path)):
        raise HTTPException(status_code=418, detail="Invalid path")

