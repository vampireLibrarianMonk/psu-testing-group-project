import subprocess

# Base URL for the Flask app
BASE_URL = "http://localhost:5001"

def test_status_102():
    command = ["http", "--check-status", "GET", f"{BASE_URL}/status/102"]
    process = subprocess.run(command, capture_output=True, text=True)

    # Check for the exact response with no content after the status line
    assert process.stdout.strip() == "", "Failed: Expected 102 no content"

def test_status_200():
    command = ["http", "--check-status", "GET", f"{BASE_URL}/status/200"]
    process = subprocess.run(command, capture_output=True, text=True)
    assert 'SUCCESS' in process.stdout.upper(), "Failed: Expected Success JSON message in response"


def test_status_302():
    command = ["http", "--follow", "GET", f"{BASE_URL}/status/302"]
    process = subprocess.run(command, capture_output=True, text=True)

    # Verify that following the redirect results in a 200 OK response with the expected success message
    assert 'SUCCESS' in process.stdout.upper(), "Failed: Expected success message in the redirected response"

def test_status_404():
    command = ["http", "--check-status", "GET", f"{BASE_URL}/status/404"]
    process = subprocess.run(command, capture_output=True, text=True)
    assert 'NOT FOUND' in process.stdout.upper(), "Failed: Expected 'NOT FOUND' error message in response"
    assert '404' in process.stderr.upper(), "Failed: Expected '404' error message in response"

def test_status_500():
    command = ["http", "--check-status", "GET", f"{BASE_URL}/status/500"]
    process = subprocess.run(command, capture_output=True, text=True)
    assert 'INTERNAL SERVER ERROR' in process.stdout.upper(), "Failed: Expected 'INTERNAL SERVER ERROR' error message in response"
    assert '500' in process.stderr.upper(), "Failed: Expected '500' error message in response"
# Run tests
test_status_102()
test_status_200()
test_status_302()
test_status_404()
test_status_500()
print("All tests passed.")
