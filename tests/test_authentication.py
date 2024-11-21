import unittest
import subprocess

class TestAuthentication(unittest.TestCase):
    BASE_URL = "http://localhost:5001"

    def run_httpie_command(self, command):
        """
        Helper function to run HTTPie commands via subprocess.
        """
        return subprocess.run(command, capture_output=True, text=True)

    def test_status_102(self):
        command = ["http", "--check-status", "GET", f"{self.BASE_URL}/status/102"]
        process = self.run_httpie_command(command)
        self.assertIn("processing", process.stdout.strip().lower(), "Failed: Expected 102 no content")

    def test_status_200(self):
        command = ["http", "--check-status", "GET", f"{self.BASE_URL}/status/200"]
        process = self.run_httpie_command(command)
        self.assertIn('SUCCESS', process.stdout.upper(), "Failed: Expected Success JSON message in response")

    def test_status_302(self):
        command = ["http", "--follow", "GET", f"{self.BASE_URL}/status/302"]
        process = self.run_httpie_command(command)
        self.assertIn('SUCCESS', process.stdout.upper(), "Failed: Expected success message in the redirected response")

    def test_status_404(self):
        command = ["http", "--check-status", "GET", f"{self.BASE_URL}/status/404"]
        process = self.run_httpie_command(command)
        self.assertIn('NOT FOUND', process.stdout.upper(), "Failed: Expected 'NOT FOUND' error message in response")
        self.assertIn('404', process.stderr.upper(), "Failed: Expected '404' error message in response")

    def test_status_500(self):
        command = ["http", "--check-status", "GET", f"{self.BASE_URL}/status/500"]
        process = self.run_httpie_command(command)
        self.assertIn('INTERNAL SERVER ERROR', process.stdout.upper(), "Failed: Expected 'INTERNAL SERVER ERROR' error message in response")
        self.assertIn('500', process.stderr.upper(), "Failed: Expected '500' error message in response")

    def test_authentication(self):
        """
        Tests HTTPie's support for Basic Authentication.
        """
        url = f"{self.BASE_URL}/test/basic-auth"

        # Test correct credentials
        result = self.run_httpie_command(["http", "--auth", "user1:password", "GET", url])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Basic Auth successful", result.stdout)

        # Test incorrect credentials
        result = self.run_httpie_command(["http", "--auth", "wrong:creds", "GET", url])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Unauthorized", result.stdout)


if __name__ == "__main__":
    unittest.main()
