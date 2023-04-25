import pytest
import subprocess
import time
import shlex

@pytest.fixture(scope="module", autouse=True)  # Change the scope to "module"
def start_server():
    print("Starting server...")  # Optional: Add this line for debugging
    server_command = "uvicorn oai_monarch_plugin.main:app --host 0.0.0.0 --port 3333"
    server_process = subprocess.Popen(shlex.split(server_command))

    # Give the server some time to start before running the tests
    time.sleep(5)

    yield

    # Clean up the server process after tests have run
    server_process.terminate()
    server_process.wait()
