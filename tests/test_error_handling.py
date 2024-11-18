import unittest
import subprocess
import json


class TestHTTPieIntegration(unittest.TestCase):
    """
    This test suite validates the Flask app endpoints using HTTPie CLI commands.
    """

    def run_httpie(self, method, url, allow_redirects=True):
        """
        Helper to run HTTPie commands via subprocess.
        """
        try:
            args = ['http', method, url]
            if not allow_redirects:
                # Do not include --follow if redirects should not be followed
                args.append('--headers')  # Adds extra detail to verify status codes
            result = subprocess.run(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout, result.stderr, result.returncode
        except FileNotFoundError:
            self.fail("HTTPie is not installed or not in PATH")

    def test_100_informational_httpie(self):
        """
        Test 102 Processing response using HTTPie.
        """
        stdout, stderr, returncode = self.run_httpie('GET', 'http://localhost:5001/status/102')

        # HTTPie should succeed in sending the request (returncode = 0)
        self.assertEqual(returncode, 0)

        # Expect no response body for informational 102 Processing
        self.assertIn('processing', stdout.lower())
        self.assertEqual('', stderr.strip())

    def test_200_success_httpie(self):
        """
        Test 200 OK response using HTTPie.
        """
        stdout, stderr, returncode = self.run_httpie('GET', 'http://localhost:5001/status/200')
        self.assertEqual(returncode, 0)
        response_json = json.loads(stdout)
        self.assertEqual(response_json, {"message": "Success"})

    def test_302_redirection_httpie(self):
        """
        Test 302 Found response using HTTPie without following redirects.
        """
        stdout, stderr, returncode = self.run_httpie('GET', 'http://localhost:5001/status/302', allow_redirects=False)

        # HTTPie should succeed in sending the request
        self.assertEqual(returncode, 0)

        # Ensure the redirection message is in the output (case insensitive)
        response_output = stdout.lower()  # Normalize case for robustness
        self.assertIn('302 found', response_output)

    def test_404_client_error_httpie(self):
        """
        Test 404 Not Found response using HTTPie.
        """
        stdout, stderr, returncode = self.run_httpie('GET', 'http://localhost:5001/status/404')
        self.assertEqual(returncode, 0)
        response_json = json.loads(stdout)
        self.assertEqual(response_json, {"error": "Not Found"})

    def test_500_server_error_httpie(self):
        """
        Test 500 Internal Server Error response using HTTPie.
        """
        stdout, stderr, returncode = self.run_httpie('GET', 'http://localhost:5001/status/500')

        # HTTPie should succeed in sending the request
        self.assertEqual(returncode, 0)

        # Ensure the server error message is in the output
        response_json = json.loads(stdout)
        self.assertEqual(response_json, {"error": "Internal Server Error"})


if __name__ == "__main__":
    unittest.main()
