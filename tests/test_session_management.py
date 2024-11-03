import unittest
import subprocess
import os
import json

from flask_app.app import tokenValue


class TestSessionManagement(unittest.TestCase):
    """
    A unittest-based test suite for validating session management using the HTTPie CLI.

    This suite tests various aspects of session handling, such as header persistence,
    session reuse, named sessions, anonymous sessions, and read-only session modes.
    It uses subprocess to run HTTPie commands and checks the responses to ensure
    correct functionality.

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

        Description:
            Verifies that custom headers are correctly persisted in a session file
            and reused across multiple requests.

        Steps:
            1. Create a session with a custom 'Authorization' header.
            2. Reuse the session and check if the header is still present.

        Assertions:
            - Checks if the expected message indicating header reception is in the response.
        """
        subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers', f'Authorization:Bearer {self.tokenValue}'])
        result = subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers'], capture_output=True)
        self.assertIn('"Authorization header received"', result.stdout.decode())

    def test_session_reuse_cli(self):
        """
        Test session reuse and authentication using the HTTPie CLI.

        Description:
            Ensures that a session can be reused for maintaining authentication details
            across requests.

        Steps:
            1. Create a session with authentication details.
            2. Reuse the session and verify if the authentication details persist.

        Assertions:
            - Checks if the response indicates that the 'Authorization' header was received.
        """
        subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers', f'Authorization:Bearer {self.tokenValue}'])
        result = subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers'], capture_output=True)
        self.assertIn('"Authorization header received"', result.stdout.decode())

    def test_named_session_cli(self):
        """
        Test named session management using the HTTPie CLI.

        Description:
            Verifies that named sessions are created and stored correctly, using
            authentication credentials.

        Steps:
            1. Create a named session with basic authentication credentials.
            2. Check if the named session file has been created successfully.

        Assertions:
            - Checks if the named session file exists on the filesystem.
        """
        subprocess.run(['http', '--session=' + self.named_session_path, '-a', 'user1:password', f'{self.base_url}/test/headers'])
        self.assertTrue(os.path.exists(self.named_session_path))

    def test_anonymous_session_cli(self):
        """
        Test anonymous session handling using the HTTPie CLI.

        Description:
            Ensures that headers persist when using anonymous sessions that are reused
            across multiple hosts.

        Steps:
            1. Create an anonymous session with a custom 'Authorization' header.
            2. Reuse the session and verify if the header persists.

        Assertions:
            - Checks if the response contains the expected message indicating header reception.
        """
        subprocess.run(['http', '--session=/tmp/anon_session.json', f'{self.base_url}/test/headers', f'Authorization:Bearer {self.userValue}'])
        result = subprocess.run(['http', '--session=/tmp/anon_session.json', f'{self.base_url}/test/headers'], capture_output=True)
        self.assertIn('"Authorization header received"', result.stdout.decode())

    def test_readonly_session_cli(self):
        """
        Test read-only session handling using the HTTPie CLI.

        Description:
            Validates that session data remains unchanged when loaded in read-only mode,
            ensuring the integrity of the session.

        Steps:
            1. Create a session with authentication details.
            2. Load the session in read-only mode and verify if the header is still present.

        Assertions:
            - Checks if the response indicates that the 'Authorization' header was received.
        """
        subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers', f'Authorization:Bearer {self.tokenValue}'])
        result = subprocess.run(['http', '--session-read-only=' + self.session_path, f'{self.base_url}/test/headers'], capture_output=True)
        self.assertIn('"Authorization header received"', result.stdout.decode())

    def test_session_file_contents(self):
        """
        Test the contents of the session file.

        Description:
            Verifies that the session file is created correctly and contains the
            expected headers and authentication data.

        Steps:
            1. Create a session with a custom 'Authorization' header.
            2. Read the session file and verify its contents.

        Assertions:
            - Checks if the session file contains the 'Authorization' header with the correct value.
        """
        subprocess.run(['http', '--session=' + self.session_path, f'{self.base_url}/test/headers',
                        f'Authorization:Bearer {self.tokenValue}'])
        with open(self.session_path, 'r') as file:
            session_data = json.load(file)

        # Extract headers as a dictionary for easier lookup
        headers_dict = {header['name']: header['value'] for header in session_data['headers']}

        # Assert that 'Authorization' header exists and has the correct value
        self.assertIn('Authorization', headers_dict)
        self.assertEqual(headers_dict['Authorization'], f'Bearer {tokenValue}')

    def test_invalid_session_path(self):
        """
        Test behavior with an invalid session file path.

        Description:
            Verifies that HTTPie handles invalid session paths gracefully and
            does not create an unexpected session file.

        Steps:
            1. Attempt to create a session with an invalid path.
            2. Check if the invalid session file path does not exist.

        Assertions:
            - Checks that the invalid session file path does not exist.
        """
        invalid_path = '/invalid/path/to/session.json'
        subprocess.run(['http', '--session=' + invalid_path, f'{self.base_url}/test/headers', f'Authorization:Bearer {self.tokenValue}'], capture_output=True)
        self.assertFalse(os.path.exists(invalid_path))

    def tearDown(self):
        """
        Cleanup method to remove session files after each test.

        Deletes:
            - The default session file (self.session_path).
            - The named session file (self.named_session_path).
            - The anonymous session file (/tmp/anon_session.json).

        This ensures a clean environment for subsequent tests by removing any
        residual session data.
        """
        if os.path.exists(self.session_path):
            os.remove(self.session_path)
        if os.path.exists(self.named_session_path):
            os.remove(self.named_session_path)
        if os.path.exists('/tmp/anon_session.json'):
            os.remove('/tmp/anon_session.json')

if __name__ == "__main__":
    unittest.main()
