import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from raga import TestSession, RagaSchema
from raga.dataset import Dataset
class TestDataset(unittest.TestCase):

    def setUp(self):
        self.test_session = TestSession("project_name", "run_name")
        self.test_session.project_id = "project_id"
        self.test_session.token = "token"
        self.dataset_name = "my_dataset"
        self.test_session.experiment_id = "experiment_id"
        self.dataset_creds = None
        self.dataset = Dataset(self.test_session, self.dataset_name, self.dataset_creds)
        self.dataset.dataset_id = "12345"

    def test_create_dataset(self):
        expected_dataset_id = "12345"
        mock_create_dataset = MagicMock(return_value={"data": {"id": expected_dataset_id}})
        self.test_session.http_client.post = mock_create_dataset

        dataset_id = self.dataset.create_dataset()

        self.assertEqual(dataset_id, expected_dataset_id)
        mock_create_dataset.assert_called_once_with(
            "api/dataset",
            {"name": self.dataset_name, "projectId": self.test_session.project_id},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )

    def test_create_dataset_file(self):
        expected_file_id = "12345"
        mock_create_dataset_file = MagicMock(return_value={"data": {"id": expected_file_id}})
        self.test_session.http_client.post = mock_create_dataset_file

        file_id = self.dataset.create_dataset_file("path/to/file.csv")

        self.assertEqual(file_id, expected_file_id)
        mock_create_dataset_file.assert_called_once_with(
            "api/dataset/file",
            {"datasetId": self.dataset.dataset_id, "filePath": "path/to/file.csv"},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )

    def test_create_dataset_columns(self):
        expected_columns = [
            {
                "name": "image_id",
                "model": "",
                "type": "prediction",
                "description": "",
            },
            {
                "name": "label_name",
                "model": "label_name",
                "type": "inferences",
                "description": "",
            },
            {
                "name": "col_name",
                "model": "label_name",
                "type": "roi",
                "description": "",
            }
        ]
        mock_create_dataset_columns = MagicMock(return_value={"data": expected_columns})
        self.test_session.http_client.post = mock_create_dataset_columns

        columns = self.dataset.create_dataset_columns(expected_columns)

        self.assertEqual(columns, expected_columns)
        mock_create_dataset_columns.assert_called_once_with(
            "api/dataset/columns",
            {"datasetId": self.dataset.dataset_id, "columns": expected_columns},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )

    def test_get_pre_signed_s3_url(self):
        expected_signed_upload_path = "https://s3.amazonaws.com/my-bucket/upload"
        expected_file_path = "my-bucket/folder/file.zip"
        mock_get_pre_signed_url = MagicMock(return_value={"data": {"signedUploadPath": expected_signed_upload_path, "filePath": expected_file_path}})
        self.test_session.http_client.get = mock_get_pre_signed_url

        signed_upload_path, file_path = self.dataset.get_pre_signed_s3_url("file.zip")

        self.assertEqual(signed_upload_path, expected_signed_upload_path)
        self.assertEqual(file_path, expected_file_path)
        mock_get_pre_signed_url.assert_called_once_with(
            "api/dataset/uploadpath",
            None,
            {"experimentId": self.test_session.experiment_id, "fileName": "file.zip", "contentType":"application/zip"},
            {"Authorization": f'Bearer {self.test_session.token}'},
        )


    def test_create_dataset(self):
        mock_post = MagicMock(return_value={"data": {"id": "dataset_id"}})
        self.test_session.http_client.post = mock_post

        dataset_id = self.dataset.create_dataset()

        mock_post.assert_called_once_with(
            "api/dataset",
            {"name": "my_dataset", "projectId": "project_id"},
            {"Authorization": "Bearer token"},
        )
        self.assertEqual(dataset_id, "dataset_id")

    def test_create_dataset_file(self):
        self.dataset.dataset_id = "dataset_id"
        mock_post = MagicMock(return_value={"data": {"id": "file_id"}})
        self.test_session.http_client.post = mock_post

        file_id = self.dataset.create_dataset_file("file_path")

        mock_post.assert_called_once_with(
            "api/dataset/file",
            {"datasetId": "dataset_id", "filePath": "file_path"},
            {"Authorization": "Bearer token"},
        )
        self.assertEqual(file_id, "file_id")

    def test_create_dataset_columns(self):
        self.dataset.dataset_id = "dataset_id"
        columns = [
            {
                "name": "image_id",
                "model": "",
                "type": "prediction",
                "description": "",
            },
            {
                "name": "label_name",
                "model": "label_name",
                "type": "inferences",
                "description": "",
            },
            {
                "name": "col_name",
                "model": "label_name",
                "type": "roi",
                "description": "",
            },
        ]
        mock_post = MagicMock(return_value={"data": "columns_data"})
        self.test_session.http_client.post = mock_post

        result = self.dataset.create_dataset_columns(columns)

        mock_post.assert_called_once_with(
            "api/dataset/columns",
            {"datasetId": "dataset_id", "columns": columns},
            {"Authorization": "Bearer token"},
        )
        self.assertEqual(result, "columns_data")

    def test_create_dataset_load_definition(self):
        self.dataset.dataset_id = "dataset_id"
        dataset_file_id = "file_id"
        file_path = "file_path"
        data_type = "pandas"
        arguments = {"arg1": "value1", "arg2": "value2"}
        mock_post = MagicMock(return_value={"data": "load_definition_data"})
        self.test_session.http_client.post = mock_post

        result = self.dataset.create_dataset_load_definition(dataset_file_id, file_path, data_type, arguments)

        mock_post.assert_called_once_with(
            "api/dataset/definition",
            {
                "datasetId": "dataset_id",
                "dataset_file_id": "file_id",
                "filePath": "file_path",
                "type": "pandas",
                "arguments": {"arg1": "value1", "arg2": "value2"},
            },
            {"Authorization": "Bearer token"},
        )
        self.assertEqual(result, "load_definition_data")

    def test_load_with_file_path(self):
        file_path = "data.csv"
        format = "csv"
        image_id = "image_id"
        type = "prediction"
        label_name = "label_name"
        col_name = "col_name"
        class_map = {"class1": 0, "class2": 1}
        self.dataset.load_labels_from_file = MagicMock()

        self.dataset.load(data=file_path, format=format, image_id=image_id, type=type,
                          label_name=label_name, col_name=col_name, class_map=class_map)

        self.dataset.load_labels_from_file.assert_called_once_with(
            file_path, format, image_id, type, label_name, col_name, class_map
        )

    # def test_load_with_data_frame_and_schema(self):
    #     data_frame = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    #     schema = RagaSchema()
    #     dataset_column = [{"name": "col1", "model": "", "type": "prediction", "description": ""}]
    #     self.dataset.load_data_frame = MagicMock()
    #     self.dataset.get_dataset_column = MagicMock(return_value=dataset_column)

    #     self.dataset.load(data=data_frame, schema=schema)

    #     self.dataset.get_dataset_column.assert_called_once_with(schema)
    #     self.dataset.load_data_frame.assert_called_once_with(data_frame, dataset_column)

    def test_load_with_invalid_data_argument(self):
        invalid_data = 123

        with self.assertRaises(ValueError):
            self.dataset.load(data=invalid_data)

    def test_load_with_invalid_schema_argument(self):
        data_frame = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        invalid_schema = "invalid_schema"

        with self.assertRaises(ValueError):
            self.dataset.load(data=data_frame, schema=invalid_schema)

    def test_load_with_invalid_schema_instance(self):
        data_frame = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        invalid_schema = RagaSchema()  # Empty schema object
        self.dataset.get_dataset_column = MagicMock()

        with self.assertRaises(ValueError):
            self.dataset.load(data=data_frame, schema=invalid_schema)

        self.dataset.get_dataset_column.assert_not_called()

    @patch("raga.dataset.create_csv_and_zip_from_data_frame")
    @patch("raga.dataset.upload_file")
    @patch("raga.dataset.delete_files")
    @patch("raga.dataset.Dataset.create_dataset_file")
    @patch("raga.dataset.Dataset.create_dataset_load_definition")
    @patch("raga.dataset.Dataset.create_dataset_columns")
    @patch("raga.dataset.Dataset.notify_server")
    @patch("raga.dataset.Dataset.get_pre_signed_s3_url")
    def test_load_data_frame(self, mock_get_pre_signed_s3_url, mock_notify_server, mock_create_dataset_columns,
                             mock_create_dataset_load_definition, mock_create_dataset_file, mock_delete_files,
                             mock_upload_file, mock_create_csv_and_zip_from_data_frame):
        data_frame = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        dataset_column = [{"name": "col1", "model": "", "type": "prediction", "description": ""}]
        csv_file = "experiment_experiment_id.csv"
        zip_file = "experiment_experiment_id.zip"
        signed_upload_path = "https://example.com/upload"
        file_path = "path/to/zip_file"
        dataset_file_id = "dataset_file_123"

        mock_get_pre_signed_s3_url.return_value = signed_upload_path, file_path
        mock_create_csv_and_zip_from_data_frame.return_value = None
        mock_upload_file.return_value = None
        mock_delete_files.return_value = None
        mock_create_dataset_file.return_value = dataset_file_id
        mock_create_dataset_load_definition.return_value = None
        mock_create_dataset_columns.return_value = None
        mock_notify_server.return_value = None

        self.dataset.load_data_frame(data_frame, dataset_column)

        mock_create_csv_and_zip_from_data_frame.assert_called_once_with(data_frame, csv_file, zip_file)
        mock_get_pre_signed_s3_url.assert_called_once_with(zip_file)
        mock_upload_file.assert_called_once_with(signed_upload_path, zip_file, success_callback=self.dataset.on_upload_success,
                                                 failure_callback=self.dataset.on_upload_failed)
        mock_delete_files.assert_called_once_with(csv_file, zip_file)
        mock_create_dataset_file.assert_called_once_with(file_path)
        mock_create_dataset_load_definition.assert_called_once_with(dataset_file_id, file_path, "pandas", dataset_column)
        mock_create_dataset_columns.assert_called_once_with(dataset_column)
        mock_notify_server.assert_called_once()


if __name__ == "__main__":
    unittest.main()
