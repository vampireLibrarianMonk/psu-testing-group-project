import subprocess
import unittest
import multiprocessing
import json
import tempfile

BASE_URL = "http://127.0.0.1:5001"  # URL of the running Flask app


class TestPerformance(unittest.TestCase):
    """
    Test suite to evaluate server performance and HTTPie functionality.
    """

    def run_httpie_command(self, args):
        """Helper function to run an HTTPie command and parse JSON response.

        - Uses subprocess to execute HTTPie CLI commands.
        - Parses the response as JSON if possible; otherwise, returns the raw output.
        """
        result = subprocess.run(args, capture_output=True, text=True)
        # Check if result is JSON and only then parse, else return raw output
        try:
            return json.loads(result.stdout) if result.returncode == 0 else result.stderr
        except json.JSONDecodeError:
            return result.stdout  # Return raw text for non-JSON responses

    def test_high_volume_requests(self):
        """
        Sends 100 concurrent GET requests to the /status/200 endpoint using HTTPie.
        Ensures all responses are 200 OK.
        """
        url = f"{BASE_URL}/status/200"

        def send_request():
            # Use the helper method to execute the HTTPie command
            result = self.run_httpie_command(["http", "GET", url])
            if isinstance(result, dict):
                self.assertEqual(result.get("message", ""), "Success")  # Check JSON content
            else:
                self.assertIn("200 OK", result)  # Check raw output

        # Run 100 requests concurrently
        processes = []
        for _ in range(100):
            p = multiprocessing.Process(target=send_request)
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

    def test_file_upload_size_limits(self):
        """Test a POST request with payload sizes increasing in increments of 5 MB, up to 20 MB. This hasw been tested
        to 500 MB incrementing in 250 MB chunks just for giggles and to see if Github Issue #35 was reproducible.

        - This test writes the payload to a temporary file in chunks and uses HTTPie's @ notation
          to avoid exceeding the argument list length limit imposed by the operating system.
        """
        error_detected = False
        max_size_mb = 20  # Maximum payload size in MB
        step_size_mb = 5  # Step size in MB
        chunk_size_mb = 1  # Chunk size in MB

        # Convert MB to characters (1 MB = 1,000,000 characters)
        max_size = max_size_mb * 1000000
        step_size = step_size_mb * 1000000
        chunk_size = chunk_size_mb * 1000000

        for size in range(step_size, max_size + 1, step_size):
            with self.subTest(payload_size=f"{size // 1000000} MB"):
                # Create a temporary file and write the payload in chunks
                with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                    chunks = size // chunk_size
                    remainder = size % chunk_size

                    # Write full chunks of 1 MB each
                    for _ in range(chunks):
                        temp_file.write('a' * chunk_size)

                    # Write any remaining characters
                    if remainder:
                        temp_file.write('a' * remainder)

                    temp_file_name = temp_file.name

                # Use the @ notation to read the payload from the file
                response = self.run_httpie_command([
                    'http', '--ignore-stdin', 'POST', 'https://httpbin.org/post', f'@{temp_file_name}'
                ])

                # Check if the response contains an error message or an indication of failure
                if "error" in response or isinstance(response, str):
                    error_detected = True
                    print(f"Error detected at payload size: {size // 1000000} MB")
                    break  # Exit loop when the error threshold is reached

        # Assert that no error was detected and the test was successful
        self.assertFalse(error_detected,
                         "No error encountered: HTTPie handled all payload sizes up to 200 MB successfully.")

if __name__ == "__main__":
    unittest.main()
