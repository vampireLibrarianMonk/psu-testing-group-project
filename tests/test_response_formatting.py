import unittest
from unittest.mock import MagicMock, patch


def format_response(response):
    """Simulates HTTPie-style response formatting."""
    status_line = f"HTTP/1.1 {response.status_code} OK"
    headers = "\n".join(f"{key}: {value}" for key, value in response.headers.items())
    body = response.text if response.text else response.json()
    return f"{status_line}\n{headers}\n\n{body}"


class TestResponseFormatting(unittest.TestCase):
    """
    This test suite checks the formatting of different types of HTTP responses,
    ensuring JSON and HTML content is handled as expected.
    """

    @patch('httpie.core.send_request')
    def test_json_response_formatting(self, mock_send_request):
        """
        Test JSON response formatting:
        - Mocks a JSON response with a 200 OK status.
        - Validates that the JSON content ("message": "Hello, World!") is correctly formatted in the output.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.json.return_value = {"message": "Hello, World!"}
        mock_response.text = None  # JSON content overrides text
        mock_send_request.return_value = mock_response

        # Simulate the response formatting
        response = format_response(mock_response)
        self.assertIn("HTTP/1.1 200 OK", response)
        self.assertIn("Content-Type: application/json", response)
        self.assertIn('"message": "Hello, World!"', response)

    def test_html_response_formatting(self):
        """
        Test HTML response formatting:
        - Mocks an HTML response with a 200 OK status.
        - Verifies that HTML content ("<html><body>Hello</body></html>") is present in the formatted response output.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_response.text = "<html><body>Hello</body></html>"
        mock_response.json.side_effect = ValueError("No JSON content")  # Simulate JSON parsing failure

        # Simulate the response formatting
        response = format_response(mock_response)
        self.assertIn("HTTP/1.1 200 OK", response)
        self.assertIn("Content-Type: text/html", response)
        self.assertIn("<html><body>Hello</body></html>", response)

    def test_error_response_formatting(self):
        """
        Test formatting for error responses:
        - Mocks a 404 Not Found response.
        - Ensures error messages and status codes are correctly displayed.
        """
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.text = None
        mock_response.json.return_value = {"error": "Not Found"}

        # Simulate the response formatting
        response = format_response(mock_response)
        self.assertIn("HTTP/1.1 404 Not Found", response)
        self.assertIn("Content-Type: application/json", response)
        self.assertIn('"error": "Not Found"', response)


if __name__ == "__main__":
    unittest.main()
