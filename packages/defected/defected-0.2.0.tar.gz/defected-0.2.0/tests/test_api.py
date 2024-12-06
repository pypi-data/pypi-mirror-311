import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd

from defected.api import analyze_timezones, extract_git_logs, parse_logs


class TestDefected(unittest.TestCase):

    @patch("subprocess.run")
    def test_extract_git_logs(self, mock_subprocess):
        """
        Test the extraction of Git logs.
        """
        # Mock subprocess result
        mock_subprocess.return_value = MagicMock(
            stdout="Alice|alice@example.com|2024-11-27 13:05:51 +0100\n"
            "Bob|bob@example.com|2024-11-26 15:30:00 -0500\n",
            returncode=0,
        )

        # Call the function
        logs = extract_git_logs("/path/to/repo")

        # Verify the results
        self.assertEqual(len(logs), 2)
        self.assertIn("Alice|alice@example.com|2024-11-27 13:05:51|+0100", logs)
        self.assertIn("Bob|bob@example.com|2024-11-26 15:30:00|-0500", logs)

    def test_parse_logs(self):
        """
        Test the parsing of logs into structured data.
        """
        # Input logs
        logs = [
            "Alice|alice@example.com|2024-11-27 13:05:51|+0100",
            "Bob|bob@example.com|2024-11-26 15:30:00|-0500",
        ]

        # Call the function
        df = parse_logs(logs)

        # Verify the results
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]["author"], "Alice")
        self.assertEqual(df.iloc[0]["email"], "alice@example.com")
        self.assertEqual(df.iloc[0]["timezone"], "+0100")
        self.assertEqual(df.iloc[1]["author"], "Bob")
        self.assertEqual(df.iloc[1]["timezone"], "-0500")

    def test_analyze_timezones(self):
        """
        Test the analysis of timezone changes.
        """
        # Create a mock DataFrame
        data = {
            "author": ["Alice", "Alice", "Alice", "Bob", "Bob"],
            "email": [
                "alice@example.com",
                "alice@example.com",
                "alice@example.com",
                "bob@example.com",
                "bob@example.com",
            ],
            "date": [
                datetime(2024, 11, 27, 13, 0, 0),
                datetime(2024, 11, 28, 14, 0, 0),
                datetime(2024, 11, 29, 15, 0, 0),
                datetime(2024, 11, 26, 12, 0, 0),
                datetime(2024, 11, 27, 12, 0, 0),
            ],
            "timezone": ["+0100", "+0200", "+0100", "-0500", "-0500"],
        }
        df = pd.DataFrame(data)

        # Call the function
        result = analyze_timezones(df, threshold=1)

        # Verify the results
        self.assertEqual(len(result), 2)
        alice_row = result[result["author"] == "Alice"].iloc[0]
        bob_row = result[result["author"] == "Bob"].iloc[0]

        self.assertEqual(alice_row["timezone_changes"], 2)
        self.assertTrue(alice_row["suspicious"])
        self.assertEqual(bob_row["timezone_changes"], 0)
        self.assertFalse(bob_row["suspicious"])

    @patch("subprocess.run")
    def test_extract_git_logs_invalid(self, mock_subprocess):
        """
        Test extraction with invalid logs.
        """
        # Mock subprocess result with malformed logs
        mock_subprocess.return_value = MagicMock(
            stdout="Invalid log entry\n", returncode=0
        )

        # Call the function
        logs = extract_git_logs("/path/to/repo")

        # Verify the results
        self.assertEqual(len(logs), 0)
