import argparse
import logging
import os
import re
import shutil
import subprocess
import tempfile
from collections import defaultdict
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)

command_description = """
Analyze Git logs for timezone changes and suspicious activities.
"""
long_description = """
Analyze Git logs for timezone changes and suspicious activities.
"""


def add_arguments(parser):
    """
    Adds the argument options to the extract command parser.
    """
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.description = long_description

    parser.add_argument(
        "--repo",
        type=str,
        help="Remote Git repository URL to clone and analyze. If not provided, the current directory will be analyzed.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=2,
        help="Number of timezone changes considered suspicious (default: 2).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="timezone_analysis.csv",
        help="Output file for the analysis (default: timezone_analysis.csv).",
    )
    parser.add_argument(
        "--no-email",
        action="store_true",
        help="Disable inclusion of contributor email addresses in the analysis.",
    )
    parser.add_argument(
        "--only-suspicious",
        action="store_true",
        help="Show and save only suspicious results (default: show all results).",
    )


def extract_git_logs(repo_path):
    """
    Extract Git logs with author, email, date, and timezone information from the specified repository.
    """
    # Extract logs with %ad containing date, time, and timezone
    cmd = ["git", "-C", repo_path, "log", "--pretty=format:%an|%ae|%ad", "--date=iso"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    logs = result.stdout.splitlines()

    # Process logs to extract time zone
    processed_logs = []
    for log in logs:
        try:
            author, email, date_time = log.split("|")
            date_parts = date_time.strip().rsplit(
                " ", 1
            )  # Split date_time by the last space
            date = date_parts[0]  # Extract the date and time
            timezone = (
                date_parts[1] if len(date_parts) > 1 else "UNKNOWN"
            )  # Extract the timezone
            processed_logs.append(f"{author}|{email}|{date}|{timezone}")
        except ValueError:
            continue  # Skip malformed logs
    return processed_logs


def parse_logs(logs, include_email=True):
    """
    Parse Git logs to extract relevant information.
    """
    data = []
    for log in logs:
        try:
            author, email, date, timezone = log.split("|")
            commit_date = datetime.fromisoformat(date.strip())
            entry = {
                "author": author.strip(),
                "date": commit_date,
                "timezone": timezone.strip(),
            }
            if include_email:
                entry["email"] = email.strip()
            data.append(entry)
        except ValueError:
            continue  # Skip malformed logs
    return pd.DataFrame(data)


def analyze_timezones(df, threshold):
    """
    Analyze timezones and detect frequent changes.
    """
    group_cols = ["author"]
    if "email" in df.columns:
        group_cols.append("email")

    grouped = df.groupby(group_cols)
    analysis = []

    for group_key, group in grouped:
        group = group.sort_values("date")
        timezones = group["timezone"].tolist()
        unique_timezones = set(timezones)
        timezone_changes = sum(
            1 for i in range(1, len(timezones)) if timezones[i] != timezones[i - 1]
        )

        analysis_entry = {
            "author": group_key[0],
            "total_commits": len(group),
            "unique_timezones": len(unique_timezones),
            "timezone_changes": timezone_changes,
            "suspicious": timezone_changes > threshold,
        }
        if "email" in df.columns:
            analysis_entry["email"] = group_key[1]
        analysis.append(analysis_entry)

    return pd.DataFrame(analysis)


def is_git_repository(path):
    """
    Check if the given path is a Git repository.
    """
    try:
        subprocess.run(
            ["git", "-C", path, "rev-parse"], check=True, capture_output=True, text=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def clone_repo(remote_url):
    """
    Clone the remote Git repository into a temporary directory.
    """
    temp_dir = tempfile.mkdtemp()
    subprocess.run(["git", "clone", remote_url, temp_dir], check=True)
    return temp_dir


def main(args):
    repo_path = None
    temp_dir = None
    try:
        if args.repo:
            print(f"Cloning remote repository: {args.repo}...")
            repo_path = clone_repo(args.repo)
        else:
            repo_path = os.getcwd()
            if not is_git_repository(repo_path):
                raise ValueError(
                    f"The current directory '{repo_path}' is not a Git repository."
                )

        print("Extracting Git logs...")
        logs = extract_git_logs(repo_path)
        print(f"{len(logs)} commits extracted.")

        print("Parsing logs...")
        df = parse_logs(logs, include_email=not args.no_email)
        if df.empty:
            print("No valid logs found.")
            return

        print(
            f"Analyzing timezones with a threshold of {args.threshold} timezone changes..."
        )
        analysis = analyze_timezones(df, args.threshold)

        if args.only_suspicious:
            analysis = analysis[analysis["suspicious"]]
            print("\nShowing only suspicious results:")

        print(analysis.sort_values("timezone_changes", ascending=False))

        print(f"\nSaving analysis to '{args.output}'...")
        analysis.to_csv(args.output, index=False)
        print("Analysis saved.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if temp_dir:
            print("Cleaning up temporary files...")
            shutil.rmtree(temp_dir)
