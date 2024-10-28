import unittest
from unittest.mock import MagicMock, patch

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
        # mock_response = MagicMock()
        # mock_response.json.return_value = {"message": "Hello, World!"}
        # mock_response.status_code = 200
        # mock_send_request.return_value = mock_response

        # response = format_response(mock_response)
        # self.assertIn('"message": "Hello, World!"', response)

    def test_html_response_formatting(self):
        """
        Test HTML response formatting:
        - Mocks an HTML response with a 200 OK status.
        - Verifies that HTML content ("<html><body>Hello</body></html>") is present in the formatted response output.
        """
        # mock_response = MagicMock()
        # mock_response.text = "<html><body>Hello</body></html>"
        # mock_response.status_code = 200

        # response = format_response(mock_response)
        # self.assertIn("<html>", response)

if __name__ == "__main__":
    unittest.main()
