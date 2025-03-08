import unittest
import pandas as pd
import os
from unittest.mock import patch
from core import Data

class TestData(unittest.TestCase):

    def setUp(self):
        # Patch os.listdir to simulate our instruments in the data directory
        patcher_listdir = patch("os.listdir", return_value=["AARTIIND.csv"])
        self.mock_listdir = patcher_listdir.start()
        self.addCleanup(patcher_listdir.stop)
        
        # Create a mock DataFrame that simulates reading the CSV file
        self.mock_df = pd.DataFrame({
            "DATETIME": ["21-08-2023 09:15", "22-08-2023 09:15", "23-08-2023 09:15"],
            "OPEN": [500, 502, 508],
            "HIGH": [505, 510, 515],
            "LOW": [495, 500, 505],
            "CLOSE": [502, 508, 512]
        })
        # Patch pd.read_csv to return the mock DataFrame for any file read
        patcher_read_csv = patch("pandas.read_csv", return_value=self.mock_df)
        self.mock_read_csv = patcher_read_csv.start()
        self.addCleanup(patcher_read_csv.stop)
        
        # Initialize the Data instance with a fake data path
        self.data_path = "/mock/path"
        self.data = Data(self.data_path)

    def test_get_raw_prices(self):
        """Test that raw prices are loaded correctly."""
        df = self.data.get_raw_prices("AARTIIND")
        self.assertEqual(len(df), 3)
        self.assertIn("DATETIME", df.columns)

    def test_prices_with_start_date(self):
        """Test filtering with start_date."""
        df = self.data.prices("AARTIIND", start_date="22-08-2023")
        # Should return 2 rows: those with dates 22-08-2023 and 23-08-2023
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]["DATETIME"], pd.Timestamp("2023-08-22"))

    def test_prices_with_end_date(self):
        """Test filtering with end_date."""
        df = self.data.prices("AARTIIND", end_date="22-08-2023")
        # Should return 2 rows: those with dates 21-08-2023 and 22-08-2023
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[-1]["DATETIME"], pd.Timestamp("2023-08-22"))

    def test_prices_with_start_and_end_date(self):
        """Test filtering with both start_date and end_date."""
        df = self.data.prices("AARTIIND", start_date="22-08-2023", end_date="22-08-2023")
        # Should return exactly 1 row for 22-08-2023
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["DATETIME"], pd.Timestamp("2023-08-22"))

    def test_invalid_instrument(self):
        """Test that requesting an invalid instrument raises ValueError."""
        with self.assertRaises(ValueError):
            self.data.get_raw_prices("INVALID")

    def test_cache_functionality(self):
        """Test that caching prevents reloading the CSV multiple times."""
        with patch("pandas.read_csv") as mock_read_csv:
            self.data.get_raw_prices("AARTIIND")
            self.data.get_raw_prices("AARTIIND")
            mock_read_csv.assert_called_once()

    def test_invalid_date_range(self):
        """Test that an invalid date range raises ValueError."""
        with self.assertRaises(ValueError):
            self.data.prices("AARTIIND", start_date="23-08-2023", end_date="21-08-2023")

if __name__ == "__main__":
    unittest.main()
