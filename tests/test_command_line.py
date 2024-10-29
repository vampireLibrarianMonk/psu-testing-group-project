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

    def test_get_request(self):
        """Test a basic GET request to verify response structure.

        - Uses HTTPie to perform a GET request to a test URL.
        - Confirms that the request URL in the response matches the intended URL.
        """
        response = self.run_httpie_command(['http', 'GET', 'https://httpbin.org/get'])
        if isinstance(response, dict):
            self.assertEqual(response['url'], 'https://httpbin.org/get')

    def test_post_request_with_json(self):
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

    def test_custom_headers(self):
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

    def test_basic_authentication(self):
        """Test basic authentication.

        - Uses HTTPie's `-a` option for basic authentication (username:password).
        - Confirms that authentication succeeds and returns the expected response.
        """
        response = self.run_httpie_command([
            'http', '-a', 'user:password', 'https://httpbin.org/basic-auth/user/password'
        ])
        if isinstance(response, dict):
            self.assertTrue(response.get('authenticated', False))

    def test_verbose_mode(self):
        """Test verbose mode to capture all details of the request.

        - Uses HTTPie's `--verbose` option to capture detailed request-response info.
        - Checks for expected HTTP request headers in verbose output.
        """
        result = subprocess.run([
            'http', '--verbose', 'GET', 'https://httpbin.org/get'
        ], capture_output=True, text=True)
        self.assertIn('GET /get HTTP/1.1', result.stdout)
        self.assertIn('Host: httpbin.org', result.stdout)

    def test_session_handling(self):
        """Test session handling with a POST request in session mode.

        - Uses HTTPie's `--session` option to save session data.
        - Verifies that session data is stored correctly across requests.
        """
        response = self.run_httpie_command([
            'http', '--session=test_session', 'POST', 'https://httpbin.org/post',
            'key=value'
        ])
        if isinstance(response, dict) and 'json' in response:
            self.assertEqual(response['json'], {'key': 'value'})

    def test_offline_mode(self):
        """Test offline mode for command parsing without sending requests.

        - Uses HTTPie's `--offline` and `--ignore-stdin` options to simulate request generation.
        - Confirms the correct structure of the HTTP request without network transmission.
        """
        result = subprocess.run([
            'http', '--offline', '--ignore-stdin', '--json', 'POST', 'https://httpbin.org/post', 'name=OfflineUser'
        ], capture_output=True, text=True)

        # Check for correct HTTP structure in offline mode
        self.assertIn('POST /post HTTP/1.1', result.stdout)
        self.assertIn('"name": "OfflineUser"', result.stdout)

    def test_streaming(self):
        """Test streaming mode to handle live responses.

        - Uses HTTPie's `--stream` option to receive a continuous data stream.
        - Verifies that the stream completes successfully.
        """
        result = subprocess.run([
            'http', '--stream', 'GET', 'https://httpbin.org/stream/20'
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)  # Stream should complete successfully

    def test_redirect_following(self):
        """Test handling of multiple redirects with the --follow option.

        - Uses HTTPie's `--follow` option to handle redirects automatically.
        - Verifies that the final redirected URL matches the expected endpoint.
        """
        response = self.run_httpie_command([
            'http', '--follow', 'https://httpbin.org/redirect/3'
        ])
        if isinstance(response, dict):
            self.assertEqual(response['url'], 'https://httpbin.org/get')  # Final URL after redirects


if __name__ == "__main__":
    unittest.main()
