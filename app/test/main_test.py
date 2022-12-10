from fastapi.testclient import TestClient
from .. import main
from .. import config
from .. import file_system as fs

from pathlib import Path

client = TestClient(main.app)

def verify_get(actual_json, expected_path):
    assert (actual_json["path"] == expected_path)
    assert (actual_json["output"] == fs.ls(Path(expected_path)))

# Test get root
def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    actual_json = response.json()
    verify_get(actual_json, config.Settings().active_path)

    # TODO: try testing with a different configured path (root dir) 

# Now try changing the default configuration path
def test_get_path():
    # TODO: factor away some of this boilerplate that we repeat
    response = client.get("/app")
    assert response.status_code == 200
    actual_json = response.json()
    verify_get(actual_json, "app")

    response = client.get("/app/test")
    assert response.status_code == 200
    actual_json = response.json()
    verify_get(actual_json, "app/test")

    # HTTP module should not allow URI to go above root
    response = client.get("/../")
    assert response.status_code == 200
    actual_json = response.json()
    verify_get(actual_json, config.Settings().active_path)

    # What happens when we ls a file?
    response = client.get(".env")
    assert response.status_code == 200
    actual_json = response.json()
    verify_get(actual_json, ".env")

    # Try with an invalid path
    response = client.get("/app/invalid")
    assert response.status_code == 418 
    assert response.json() == {"detail": "Invalid path"}

    response = client.get("*")
    assert response.status_code == 418 
    assert response.json() == {"detail": "Invalid path"}
   
TEST_PATH = Path("app/test/")

def test_delete():
    # TODO: make a directory for generated files and add it to .gitignore
    test_path = TEST_PATH / "test_file.txt"
    test_path.touch()
    assert test_path.exists()

    response = client.delete("app/test/test_file.txt") 
    assert response.status_code == 200
    assert response.json() == {"path": "app/test/test_file.txt", "output": "Deleted"}
    assert not test_path.exists()

    # use invalid path
    response = client.delete("app/test/invalid") 
    assert response.status_code == 418
    assert response.json() == {"detail": "Invalid path"}
    # TODO: ensure that nothing was deleted! :) 
