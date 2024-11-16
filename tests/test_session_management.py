import unittest
import subprocess
import os

class TestSessionManagement(unittest.TestCase):
    """
    A unittest-based test suite for validating session management using the HTTPie CLI.

    This suite tests various aspects of session handling, such as header persistence,
    session reuse, named sessions, anonymous sessions, read-only session modes, handling
    of large payloads, malformed headers, and non-persistent sessions.

    Attributes:
        base_url (str): The base URL of the Flask app being tested.
        session_path (str): The path for the default session file.
        named_session_path (str): The path for the named session file.
    """

    # Token variables for customization
    tokenValue = "sampletoken"
    userValue = "anonymousDude"

    def setUp(self):
        """
        Setup method for initializing test parameters and preparing the environment.

        Initializes:
            - self.base_url: The base URL of the Flask app.
            - self.session_path: Path for storing session data during tests.
            - self.named_session_path: Path for storing named session data.

        This method is called before each test to ensure a clean setup.
        """
        self.base_url = 'http://localhost:5001'
        self.session_path = './test_session.json'
        self.named_session_path = './named_session_user1.json'

    def test_header_persistence_cli(self):
        """
        Test header persistence using the HTTPie CLI.
        """
        subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers', f'Authorization:Bearer {self.tokenValue}'])
        result = subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers'], capture_output=True)
        self.assertIn('"Authorization header received"', result.stdout.decode())

    def test_session_reuse_cli(self):
        """
        Test session reuse and authentication using the HTTPie CLI.
        """
        subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers', f'Authorization:Bearer {self.tokenValue}'])
        result = subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers'], capture_output=True)
        self.assertIn('"Authorization header received"', result.stdout.decode())

    def test_named_session_cli(self):
        """
        Test named session management using the HTTPie CLI.
        """
        subprocess.run(['http', '--session=' + self.named_session_path, '-a', 'user1:password', f'{self.base_url}/test/headers'])
        self.assertTrue(os.path.exists(self.named_session_path))

    def test_anonymous_session_cli(self):
        """
        Test anonymous session handling using the HTTPie CLI.
        """
        subprocess.run(['http', '--session=/tmp/anon_session.json', f'{self.base_url}/test/headers', f'Authorization:Bearer {self.userValue}'])
        result = subprocess.run(['http', '--session=/tmp/anon_session.json', f'{self.base_url}/test/headers'], capture_output=True)
        self.assertIn('"Authorization header received"', result.stdout.decode())

    def test_readonly_session_cli(self):
        """
        Test read-only session handling using the HTTPie CLI.
        """
        subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers', f'Authorization:Bearer {self.tokenValue}'])
        result = subprocess.run(['http', '--session-read-only=' + self.session_path, f'{self.base_url}/test/headers'], capture_output=True)
        self.assertIn('"Authorization header received"', result.stdout.decode())

    def test_large_payload_session(self):
        """
        Test handling of large payloads in sessions.

        Verifies that the server can receive and handle large payloads without crashing or data loss.
        """
        for size_kb in range(10, 121, 10):  # Testing payloads from 10 KB to 100 KB in 10 KB increments
            with self.subTest(payload_size=f"{size_kb} KB"):
                large_payload = 'x' * (size_kb * 1024)  # Generate payload of specified size
                # Use --form (-f) to send data as form-encoded in the body
                result = subprocess.run([
                    'http', '--session=' + self.session_path, '--ignore-stdin', '-f', 'POST',
                    f'{self.base_url}/test/large_payload', f'payload={large_payload}'
                ], capture_output=True, text=True)

                # Check that the response confirms receipt of the payload
                self.assertIn("Payload received", result.stdout, f"Failed to receive payload of size {size_kb} KB")

    def test_malformed_header_in_session(self):
        """
        Test handling of malformed headers in sessions.

        Ensures that malformed headers are either rejected or handled gracefully without crashing.
        """
        malformed_header = 'Authorization:Bearer invalid@token!'  # Use an invalid format instead of a null byte
        result = subprocess.run(
            ['http', '--session=' + self.session_path, f'{self.base_url}/test/headers', malformed_header],
            capture_output=True,
            text=True
        )

        # Check that the response contains an error indicating an issue with the Authorization header
        self.assertIn("Authorization header missing or incorrect", result.stdout,
                      "Malformed header was not handled correctly")

    def test_non_persistent_session(self):
        """
        Test the behavior of non-persistent sessions by ensuring no session file is created.
        """
        result = subprocess.run(['http', f'{self.base_url}/test/headers', f'Authorization:Bearer sampletoken'], capture_output=True)
        self.assertNotIn('session', os.listdir('.'))  # Confirm that no session file was created.

    def tearDown(self):
        """
        Cleanup method to remove session files after each test.
        """
        if os.path.exists(self.session_path):
            os.remove(self.session_path)
        if os.path.exists(self.named_session_path):
            os.remove(self.named_session_path)
        if os.path.exists('/tmp/anon_session.json'):
            os.remove('/tmp/anon_session.json')

if __name__ == "__main__":
    unittest.main()