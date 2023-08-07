from typing import Optional
import pandas as pd
from raga.dataset_creds import DatasetCreds

class DatasetValidator:
    @staticmethod
    def validate_test_df(test_df: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(test_df, pd.DataFrame):
            raise TypeError("Test dataframe must be of type pd.DataFrame.")
        # Additional validation logic specific to test_df, e.g., checking required columns or shape
        return test_df

    @staticmethod
    def validate_name(name: str) -> str:
        if not name:
            raise ValueError("Name is required.")
        # Additional validation logic specific to name, e.g., checking length or format
        return name

    @staticmethod
    def validate_creds(creds: Optional[DatasetCreds] = None) -> Optional[DatasetCreds]:
        if creds is not None and not isinstance(creds, DatasetCreds):
            raise TypeError("DatasetCreds must be an instance of the DatasetCreds class.")
        # Additional validation logic specific to creds, e.g., checking authentication
        return creds
