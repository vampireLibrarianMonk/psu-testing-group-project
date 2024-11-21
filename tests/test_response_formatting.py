import unittest
import subprocess
import tempfile
import os

BASE_URL = "http://127.0.0.1:5001"  # URL of the running Flask app


class TestRequestParsing(unittest.TestCase):
    """
    Test suite for validating HTTP request parsing.
    Covers JSON, XML, CSV payloads, and multipart file uploads.
    """

    def test_post_request_with_json_file(self):
        """
        Test POST request with JSON data from a file.
        """
        url = f"{BASE_URL}/test/json"
        json_payload = '{"name": "HTTPie", "version": "3.2", "features": ["CLI", "JSON"]}'

        # Write the JSON payload to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            temp_file.write(json_payload.encode())
            temp_file_path = temp_file.name

        try:
            # Use @file to send JSON payload from the file
            result = subprocess.run(
                [
                    "http",
                    "POST",
                    url,
                    f"@{temp_file_path}",  # Correctly reference the temporary file
                    "--ignore-stdin"  # Avoid conflicts with stdin
                ],
                capture_output=True,
                text=True
            )

            # Assertions to verify subprocess behavior and HTTP response
            self.assertEqual(result.returncode, 0, "The subprocess should exit with a return code of 0.")
            self.assertIn('"method":"POST"', result.stdout, "The method should be POST.")
            self.assertIn('"Content-Type":"application/json"', result.stdout,
                          "The Content-Type should be application/json.")
            self.assertIn('"name":"HTTPie"', result.stdout, "The JSON name value should match.")
            self.assertIn('"version":"3.2"', result.stdout, "The JSON version value should match.")
            self.assertIn('"features":["CLI","JSON"]', result.stdout, "The JSON features value should match.")
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)

    def test_post_request_with_xml_file(self):
        """
        Test POST request with XML data from a file.
        """
        url = f"{BASE_URL}/test/xml"
        xml_payload = """<note>
                            <to>Bob</to>
                            <from>Patrick</from>
                            <heading>Reminder</heading>
                            <body>Don't forget xml!</body>
                         </note>"""

        # Write the XML payload to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
            temp_file.write(xml_payload.encode())
            temp_file_path = temp_file.name

        try:
            # Use @file to send XML payload from the file
            result = subprocess.run(
                [
                    "http",
                    "POST",
                    url,
                    f"@{temp_file_path}",  # Correctly reference the temporary file
                    "--ignore-stdin"
                ],
                capture_output=True,
                text=True
            )

            # Assertions to verify subprocess behavior and HTTP response
            self.assertEqual(result.returncode, 0, "The subprocess should exit with a return code of 0.")
            self.assertIn('"method":"POST"', result.stdout, "The method should be POST.")
            self.assertIn('"Content-Type":"application/xml"', result.stdout,
                          "The Content-Type should be application/xml.")
            self.assertIn('"data":{"body":"Don\'t forget xml!","from":"Patrick","heading":"Reminder","to":"Bob"}',
                          result.stdout, "The parsed XML should match the expected structure and values.")
        finally:
            os.remove(temp_file_path)

    def test_post_request_with_csv_file(self):
        """
        Test POST request with CSV data from a file.
        """
        url = f"{BASE_URL}/test/csv"
        csv_payload = "name,age,location\nPatrick,39,USA\nBob,30,UK"

        # Write the CSV payload to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(csv_payload.encode())
            temp_file_path = temp_file.name

        try:
            # Use @file to send CSV payload from the file
            result = subprocess.run(
                [
                    "http",
                    "POST",
                    url,
                    f"@{temp_file_path}",  # Correctly reference the temporary file
                    "--ignore-stdin"
                ],
                capture_output=True,
                text=True
            )

            # Assertions to verify subprocess behavior and HTTP response
            self.assertEqual(result.returncode, 0, "The subprocess should exit with a return code of 0.")
            self.assertIn('"method":"POST"', result.stdout, "The method should be POST.")
            self.assertIn('"Content-Type":"text/csv"', result.stdout,
                          "The Content-Type should be text/csv.")
            self.assertIn(
                '"data":[{"age":"39","location":"USA","name":"Patrick"},{"age":"30","location":"UK","name":"Bob"}]',
                result.stdout, "The parsed CSV should match the expected structure and values.")

        finally:
            os.remove(temp_file_path)

    def test_post_request_with_html_file(self):
        """
        Test POST request with HTML data from a file.
        """
        url = f"{BASE_URL}/test/html"
        html_payload = """<html>
                              <head><title>Test</title></head>
                              <body><p>This is a test HTML payload.</p></body>
                          </html>"""

        # Write the HTML payload to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            temp_file.write(html_payload.encode())
            temp_file_path = temp_file.name

        try:
            # Use @file to send HTML payload from the file
            result = subprocess.run(
                [
                    "http",
                    "POST",
                    url,
                    f"@{temp_file_path}",  # Correctly reference the temporary file
                    "--ignore-stdin"
                ],
                capture_output=True,
                text=True
            )

            # Assertions to verify subprocess behavior and HTTP response
            self.assertEqual(result.returncode, 0, "The subprocess should exit with a return code of 0.")
            self.assertIn('"method":"POST"', result.stdout, "The method should be POST.")
            self.assertIn('"Content-Type":"text/html"', result.stdout,
                          "The Content-Type should be text/html.")
            self.assertIn(
                '"data":"<html>\\n                              <head><title>Test</title></head>\\n                              <body><p>This is a test HTML payload.</p></body>\\n                          </html>"',
                result.stdout, "The returned HTML should match the expected structure.")

        finally:
            os.remove(temp_file_path)


if __name__ == "__main__":
    unittest.main()
