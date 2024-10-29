import unittest
import hashlib
import shutil
import subprocess
from pathlib import Path


class TestFileDownloadWithHTTPie(unittest.TestCase):
    """
    Test case for downloading a file with HTTPie, verifying its existence and checksum,
    and then cleaning up the temporary directory.
    """

    def setUp(self):
        # Set up the temporary directory path within the test directory
        # This ensures isolation for each test run and easy cleanup.
        self.temp_dir = Path(__file__).parent / "temp_download"
        self.temp_dir.mkdir(exist_ok=True)

    def calculate_md5(self, file_path):
        """Helper function to calculate the MD5 checksum of a file.
        This is used to verify the integrity of the downloaded file.
        """
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()

    def test_download_file_with_md5_check(self):
        """Test downloading a file using HTTPie, verifying it, and cleaning up.

        - This test uses HTTPie's `--download` flag to save the response content to a file.
        - The `-o` option specifies the output path for the downloaded file.
        - After the download, the test checks if the file exists and verifies its MD5 checksum
          against an expected hash value to ensure integrity.
        """
        url = 'https://httpbin.org/image/jpeg'  # Replace with the actual URL of the image
        download_path = self.temp_dir / "jpeg.jpg"

        # Use HTTPie to perform a GET request and download the file
        result = subprocess.run([
            'http', 'GET', url, '--download', '-o', str(download_path)
        ], capture_output=True, text=True)

        # Check that HTTPie ran successfully and no errors occurred
        self.assertEqual(result.returncode, 0, f"HTTPie download failed: {result.stderr}")

        # Check that the file exists at the specified download path
        self.assertTrue(download_path.exists(), "Downloaded file does not exist.")

        # Verify the downloaded file's MD5 checksum for data integrity
        expected_md5sum = 'a27095e7727c70909c910cefe16d30de'  # MD5 of the uploaded image
        downloaded_md5sum = self.calculate_md5(download_path)
        self.assertEqual(downloaded_md5sum, expected_md5sum, "MD5 checksum does not match.")

    def tearDown(self):
        # Clean up by deleting the temporary directory and its contents.
        # This ensures no leftover files between tests.
        shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    unittest.main()
