import os
import unittest
from unittest import mock
import pandas as pd
from raga import get_dataset_column, upload_file, create_csv_and_zip_from_data_frame, delete_files
from raga.utils.dataset_util import FileUploadError

class TestFileUpload(unittest.TestCase):
    
    @mock.patch("os.path.isfile")
    @mock.patch("requests.put")
    def test_upload_file(self, mock_requests_put, mock_os_path_isfile):
        # Test case for successful file upload
        pre_signed_url = "pre_signed_url"
        file_path = "/Users/manabroy/Downloads/data.json"
        success_callback = mock.Mock()
        failure_callback = mock.Mock()
        mock_os_path_isfile.return_value = True
        mock_requests_put.return_value.status_code = 200

        self.assertTrue(upload_file(pre_signed_url, file_path, success_callback, failure_callback))
        mock_requests_put.assert_called_once_with(pre_signed_url, data=mock.ANY, headers={"Content-Type": "application/zip"})
        success_callback.assert_called_once()

        # Test case for unsuccessful file upload
        mock_requests_put.return_value.status_code = 500

        with self.assertRaises(FileUploadError):
            upload_file(pre_signed_url, file_path, success_callback, failure_callback)
        failure_callback.assert_called_once_with(500)


if __name__ == "__main__":
    unittest.main()
