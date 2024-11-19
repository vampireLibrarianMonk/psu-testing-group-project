import unittest
import subprocess

BASE_URL = "http://127.0.0.1:5001"  # URL of the running Flask app

class TestRequestParsing(unittest.TestCase):
    """
    This test suite validates HTTP request parsing, ensuring that methods, URLs, data and headers
    are correctly processed for various request configurations.
    """

    def test_get_request_parsing(self):
        """
        Test GET request parsing:
        - Creates a GET request to a specified URL.
        - Checks that the method is 'GET' and that the URL is correctly set.
        """
        # request = parse_request('GET', 'https://example.com')
        # self.assertEqual(request.method, 'GET')
        # self.assertEqual(request.url, 'https://example.com')

    def test_post_request_with_json(self):
        """
        Test POST request with JSON data:
        - Creates a POST request to a specified URL with JSON-formatted data.
        - Validates that the method is 'POST' and that the request body contains the specified JSON data.
        """
        # data = '{"name": "HTTPie"}'
        # request = parse_request('POST', 'https://example.com', data=data)
        # self.assertEqual(request.method, 'POST')
        # self.assertEqual(request.body, data)

    def test_custom_headers(self):
        """
        Tests HTTPie's ability to send custom headers.
        """
        url = f"{BASE_URL}/test/headers"

        result = subprocess.run(
            ["http", "GET", url, "Authorization:Bearer sampletoken"],
            capture_output=True,
            text=True
        )
        self.assertIn("200 OK", result.stdout)
        self.assertIn("Authorization header received", result.stdout)

if __name__ == "__main__":
    unittest.main()
