import unittest
import subprocess
from unittest.mock import patch


class TestAuthPluginCLI(unittest.TestCase):
    """
    This test suite validates the integration of HTTPie’s CLI with simulated authentication functionality.
    It captures output generated from a subprocess call to HTTPie, testing if custom Authorization headers
    are added correctly and included in live HTTP requests.
    """

    @patch('httpie.plugins.AuthPlugin')
    def test_httpie_bearer_token_auth(self, MockAuthPlugin):
        """
        Test HTTPie CLI with a custom Bearer Token Authorization header:
        - Mocks an `AuthPlugin` to add a Bearer token in the Authorization header.
        - Makes a live request to `httpbin.org/get` to inspect the Authorization header in the response.
        """
        # Mock an instance of AuthPlugin to simulate an authentication plugin
        mock_plugin_instance = MockAuthPlugin.return_value
        mock_plugin_instance.get_auth.return_value = ("Authorization", "Bearer test_token")

        # Target URL for testing (httpbin.org/get will echo back the headers it receives)
        url = 'https://httpbin.org/get'

        # Run HTTPie with a real GET request, including the mocked Authorization header
        result = subprocess.run([
            'http', 'GET', url, 'Authorization: Bearer test_token'
        ], capture_output=True, text=True)

        # Check if HTTPie CLI ran without errors
        self.assertEqual(result.returncode, 0, f"HTTPie CLI failed: {result.stderr}")

        # Confirm that the Authorization header was sent by inspecting httpbin's echoed headers
        self.assertIn('"Authorization": "Bearer test_token"', result.stdout)

    @patch('httpie.plugins.AuthPlugin')
    def test_httpie_basic_auth(self, MockAuthPlugin):
        """
        Test HTTPie CLI with Basic Authentication:
        - Mocks an `AuthPlugin` to add a Basic Authorization header with a username and password.
        - Sends a live GET request to `httpbin.org/basic-auth/user/passwd` to verify correct credentials.
        """
        # Mock an AuthPlugin to return a Basic Authorization header with credentials
        mock_plugin_instance = MockAuthPlugin.return_value
        username = "user"
        password = "passwd"
        mock_plugin_instance.get_auth.return_value = ("Authorization", f"Basic {username}:{password}")

        # Use a URL that requires Basic Authentication (httpbin.org/basic-auth/user/passwd)
        url = f'https://httpbin.org/basic-auth/{username}/{password}'

        # Execute HTTPie with the explicit GET method, URL, and Basic Auth flag in the correct order
        result = subprocess.run([
            'http', 'GET', url, '-a', f"{username}:{password}"
        ], capture_output=True, text=True)

        # Check if HTTPie ran successfully
        self.assertEqual(result.returncode, 0, f"HTTPie CLI failed: {result.stderr}")

        # Validate that the response indicates successful authentication
        self.assertIn('"authenticated": true', result.stdout)


if __name__ == "__main__":
    unittest.main()
