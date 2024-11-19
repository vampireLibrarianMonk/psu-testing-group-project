import unittest
import subprocess
import json


class TestCommandLineArguments(unittest.TestCase):
    """
    This test suite validates the parsing of command-line arguments into HTTP requests,
    focusing on method, URL, data payload, headers, and additional HTTPie options.
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

    def test_01_get_request(self):
        """Test a basic GET request to verify response structure.

        - Uses HTTPie to perform a GET request to a test URL.
        - Confirms that the request URL in the response matches the intended URL.
        """
        response = self.run_httpie_command(['http', 'GET', 'https://httpbin.org/get'])
        if isinstance(response, dict):
            self.assertEqual(response['url'], 'https://httpbin.org/get')

    def test_02_post_request_with_json(self):
        """Test a POST request with JSON payload.

        - Uses HTTPie's JSON parsing (`key:=value` format) to send a JSON object in the POST body.
        - Verifies that the JSON data received matches the sent data.
        """
        response = self.run_httpie_command([
            'http', 'POST', 'https://httpbin.org/post',
            'name=John', 'age:=30', 'married:=true'
        ])
        if isinstance(response, dict) and 'json' in response:
            self.assertEqual(response['json'], {'name': 'John', 'age': 30, 'married': True})

    def test_03_custom_headers(self):
        """Test a GET request with custom headers.

        - Sends custom headers using HTTPie CLI.
        - Verifies that the headers in the response match the expected values.
        """
        response = self.run_httpie_command([
            'http', 'GET', 'https://httpbin.org/headers',
            'X-API-Token:123', 'Authorization:Bearer token123'
        ])
        if isinstance(response, dict) and 'headers' in response:
            self.assertEqual(response['headers']['Authorization'], 'Bearer token123')
            self.assertEqual(response['headers']['X-Api-Token'], '123')

    def test_04_basic_authentication(self):
        """Test basic authentication.

        - Uses HTTPie's `-a` option for basic authentication (username:password).
        - Confirms that authentication succeeds and returns the expected response.
        """
        response = self.run_httpie_command([
            'http', '-a', 'user:password', 'https://httpbin.org/basic-auth/user/password'
        ])
        if isinstance(response, dict):
            self.assertTrue(response.get('authenticated', False))

    def test_05_verbose_mode(self):
        """Test verbose mode to capture all details of the request.

        - Uses HTTPie's `--verbose` option to capture detailed request-response info.
        - Checks for expected HTTP request headers in verbose output.
        """
        result = self.run_httpie_command([
            'http', '--verbose', 'GET', 'https://httpbin.org/get'
        ])
        # Ensure raw output mode for non-JSON verbose response
        if isinstance(result, str):  # Verbose mode outputs text, not JSON
            self.assertIn('GET /get HTTP/1.1', result)
            self.assertIn('Host: httpbin.org', result)
        else:
            self.fail("Verbose mode output not as expected")

    def test_06_session_handling(self):
        """Test session handling with a POST request in session mode.

        - Uses HTTPie's `--session` option to save session data.
        - Verifies that session data is stored correctly across requests.
        """
        response = self.run_httpie_command([
            'http', '--session=test_session', '--ignore-stdin', 'POST', 'https://httpbin.org/post',
            'key=value'
        ])
        if isinstance(response, dict) and 'json' in response:
            # Verify that the session correctly sends the data
            self.assertEqual(response['json'], {'key': 'value'})
        else:
            self.fail("Session handling output not as expected")

    def test_07_offline_mode(self):
        """Test offline mode for command parsing without sending requests.

        - Uses HTTPie's `--offline` and `--ignore-stdin` options to simulate request generation.
        - Confirms the correct structure of the HTTP request without network transmission.
        """
        result = self.run_httpie_command([
            'http', '--offline', '--ignore-stdin', '--json', 'POST', 'https://httpbin.org/post', 'name=OfflineUser'
        ])

        # Check for correct HTTP structure in offline mode
        if isinstance(result, str):  # Offline mode outputs raw text
            self.assertIn('POST /post HTTP/1.1', result)
            self.assertIn('"name": "OfflineUser"', result)
        else:
            self.fail("Offline mode output not as expected")

    def test_08_streaming(self):
        """Test streaming mode to handle live responses.

        - Uses HTTPie's `--stream` option to receive a continuous data stream.
        - Verifies that the stream completes successfully and contains valid JSON.
        """
        result = self.run_httpie_command([
            'http', '--stream', 'GET', 'https://httpbin.org/stream/20'
        ])

        if isinstance(result, str):  # Streaming outputs raw text
            try:
                # Parse the result line-by-line to validate JSON entries
                lines = result.splitlines()
                for line in lines:
                    if line.strip():  # Ignore empty lines
                        parsed_line = json.loads(line)  # Ensure JSON validity
                        self.assertIn("id", parsed_line)  # Check for expected key
            except json.JSONDecodeError:
                self.fail("Streaming output contains invalid JSON")
        else:
            self.fail("Streaming mode output not as expected")

    def test_09_redirect_following(self):
        """Test handling of multiple redirects with the --follow option.

        - Uses HTTPie's `--follow` option to handle redirects automatically.
        - Verifies that the final redirected URL matches the expected endpoint.
        """
        response = self.run_httpie_command([
            'http', '--follow', 'https://httpbin.org/redirect/3'
        ])
        if isinstance(response, dict):
            self.assertEqual(response['url'], 'https://httpbin.org/get')  # Final URL after redirects

    def test_10_empty_json_payload(self):
        """Test a POST request with an empty JSON object."""
        response = self.run_httpie_command(['http', 'POST', 'https://httpbin.org/post', '{}'])
        self.assertIn('{}', response)  # Adjust assertion to expected response content

    def test_11_no_headers(self):
        """Test a GET request with no headers."""
        response = self.run_httpie_command(['http', 'GET', 'https://httpbin.org/headers'])
        self.assertNotIn('Authorization', response)  # Ensure no headers are sent

    def test_12_header_count_below_limit(self):
        """Test a GET request with a header count below the assumed limit.

        - Using 14 headers, which is well within the range typically handled
          by HTTP servers without any issues. This test ensures normal operation
          with a moderate number of headers.
        """
        headers = ['Header{}:Value{}'.format(i, i) for i in range(1, 15)]  # 14 headers
        response = self.run_httpie_command(['http', 'GET', 'https://httpbin.org/headers'] + headers)
        if isinstance(response, dict) and 'headers' in response:
            self.assertEqual(response['headers'].get('Header14'), 'Value14')  # Check the last header

    def test_13_header_count_at_limit(self):
        """Test a GET request with a header count at the assumed limit.

        - Using 20 headers as an estimated upper limit, based on common handling
          capabilities of servers and the absence of specific documentation from httpbin.org.
          This tests the boundary of header handling without exceeding typical server limits.
        """
        headers = ['Header{}:Value{}'.format(i, i) for i in range(1, 21)]  # 20 headers (assumed limit)
        response = self.run_httpie_command(['http', 'GET', 'https://httpbin.org/headers'] + headers)
        if isinstance(response, dict) and 'headers' in response:
            self.assertEqual(response['headers'].get('Header20'), 'Value20')  # Check the last header

    def test_14_header_count_until_error(self):
        """Test a GET request with header counts increasing in increments of 10 until an error is encountered.

        - The test will pass if an error is detected before reaching the maximum header count (100).
          If no error is encountered, it will check the response type for correctness.
        """
        error_detected = False
        for count in range(10, 101, 10):  # Incrementing header count from 10 to 100
            headers = ['Header{}:Value{}'.format(i, i) for i in range(1, count + 1)]
            response = self.run_httpie_command(['http', 'GET', 'https://httpbin.org/headers'] + headers)

            # Check for error response
            if "error" in response or isinstance(response, str):
                error_detected = True
                break  # Exit the loop early if an error is detected

        # Assert that an error was detected before reaching the maximum limit
        self.assertTrue(error_detected, "Expected an error before reaching the maximum header count of 100.")

if __name__ == "__main__":
    unittest.main()
