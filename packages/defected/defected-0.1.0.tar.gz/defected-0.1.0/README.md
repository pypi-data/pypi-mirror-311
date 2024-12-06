# defected

![Build](https://github.com/4383/defected/actions/workflows/python-app.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/defected.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/defected.svg)
![PyPI - Status](https://img.shields.io/pypi/status/defected.svg)
[![Downloads](https://pepy.tech/badge/defected)](https://pepy.tech/project/defected)
[![Downloads](https://pepy.tech/badge/defected/month)](https://pepy.tech/project/defected/month)

Open source projects thrive on collaboration, but their openness comes with
risks. Contributors may unknowingly or intentionally exhibit suspicious
behaviors, such as:
- Frequent timezone changes in their commit metadata.
- Working at unusual hours or during public holidays.
- Unusual patterns in commit activity.

These anomalies could indicate automation scripts, compromised accounts, or
malicious actions.

**Defected** is a CLI tool designed to help maintainers detect and flag
suspicious commit patterns. By analyzing Git logs, Defected provides insights
into contributors’ behaviors, helping ensure the security and integrity of
your project.

## Problem Statement

Risks in Open Source Collaboration:
1. **Frequent Timezone Changes**:
   - Automation scripts or account misuse can result in rapid changes in
     timezone metadata.
2. **Unusual Working Hours**:
   - Commits made during public holidays or odd hours may indicate suspicious
     activity.
3. **Behavioral Anomalies**:
   - Patterns of activity inconsistent with normal contributor behavior could
     point to automation or malicious intent.

Manually detecting these patterns is tedious and impractical for large
projects.

## Objective

Defected addresses these challenges by:
- **Detecting frequent timezone changes** in commit metadata.
- **Highlighting contributors** with irregular commit patterns.
- **Flagging potential risks** for maintainers to investigate.
- Providing **clear and exportable reports** for further analysis.

## Features

1. **Easy-to-Use CLI**:
   - Installable via PyPI, Defected is simple to run directly from your
     terminal.
2. **Commit Metadata Analysis**:
   - Extracts author, email, date, and timezone data from Git logs.
3. **Timezone Change Detection**:
   - Flags contributors exceeding a configurable threshold of timezone
     changes.
4. **Customizable Options**:
   - Adjust thresholds, filter suspicious results.
5. **Exportable Reports**:
   - Saves results in CSV format for further analysis.

## Installation

Install Defected using **pip**:

```bash
$ pip install defected
```

## Usage

Defected provides a single command-line interface with subcommands.
You can list all the available commands by using:

```bash
$ defected -h
```

### Available Commands

The `analyze` sub-command help you to find suspicious contributors:
```bash
$ defected analyze [OPTIONS]
```

List all the available options by using:
```bash
$ defected analyze -h
```

## Examples

Analyze the current repository for timezone changes:

```bash
defected analyze
```

Clone and analyze a remote repository.
Analyze a remote repository by providing its URL:

```bash
defected analyze --repo https://github.com/user/repo.git
```

Filter only suspicious results. Display and export only
contributors flagged as suspicious:

```bash
defected analyze --only-suspicious
```

## Example Output

### Terminal Output
```
Extracting Git logs...
150 commits extracted.

Analyzing timezones with a threshold of 2 timezone changes...

Showing only suspicious results:
            author             email      total_commits  unique_timezones  timezone_changes  suspicious
0    Alice Smith    alice@example.com     45              3                4                True
1    Bob Johnson    bob@example.com       30              2                3                True

Saving analysis to 'timezone_analysis.csv'...
Analysis saved.
```

### CSV Output

| author       | email             | total_commits | unique_timezones | timezone_changes | suspicious |
|--------------|-------------------|---------------|-------------------|------------------|------------|
| Alice Smith  | alice@example.com | 45            | 3                 | 4                | True       |
| Bob Johnson  | bob@example.com   | 30            | 2                 | 3                | True       |

## Real world use case

[JiaT75](https://github.com/JiaT75) and the [xz Backdoor](https://en.wikipedia.org/wiki/XZ_Utils_backdoor)

### **Background**

In February 2024, a contributor named **[JiaT75](https://github.com/JiaT75)**
managed to introduce a backdoor into the popular compression utility **xz**.
This backdoor could have allowed unauthorized access to systems using the
library, creating a serious security risk.

Upon investigation, it was discovered that **JiaT75** exhibited **suspicious behavior**:
1. They made commits from multiple, rapidly-changing timezones over a short
   period.
2. Their activity patterns were inconsistent with typical open source
   contributors, suggesting potential misuse of accounts or automation.

Defected can help identify such patterns in contributors' Git activity.

### **Detecting JiaT75's Behavior with Defected**

Suppose you have a repository of **xz** and suspect malicious activity. You
can use **Defected** to analyze the commit logs for anomalies.

Let's analyze the xz repository:
```bash
defected analyze --repo https://github.com/tukaani-project/xz --only-suspicious
```

This command output something like the following:
```
Cloning remote repository: https://github.com/tukaani-project/xz...
Extracting Git logs...
2676 commits extracted.
Parsing logs...
Analyzing timezones with a threshold of 2 timezone changes...

Showing only suspicious results:
             author  total_commits  unique_timezones  timezone_changes  suspicious                     email
36     Lasse Collin           2102                 3                36        True  lasse.collin@tukaani.org
28          Jia Tan            449                 3                14        True        jiat0218@gmail.com
32  Jonathan Nieder              9                 3                 4        True        jrnieder@gmail.com

Saving analysis to 'timezone_analysis.csv'...
Analysis saved.
```

Results are exported at the CSV format and can be loaded in sheet:

| author          | total_commits | unique_timezones  | timezone_changes | suspicious | email                     |
|-----------------|---------------|-------------------|------------------|------------|---------------------------|
| Lasse Collin    | 2102          | 3                 | 36               | True       | lasse.collin@tukaani.org  |
| Jia Tan         | 449           | 3                 | 14               | True       | jiat0218@gmail.com        |
| Jonathan Nieder | 9             | 3                 | 4                | True       | jrnieder@gmail.com        |

### Interpretation

The results show that **Jia Tan** also known as **[JiaT75](https://github.com/JiaT75)**:
- Contributed 449 commits to the repository.
- Operated from **3 different timezones** during his activity period.
- Exhibited **14 timezone changes**, exceeding the threshold of 2, which flags them as "suspicious."

These irregular patterns warrant further investigation and could have raised
red flags before the backdoor was merged.

Obviously not all activities are not suspicious. The result above also show
legit activity like the ones from Lasse and Jonathan. But the one from Jia
as been proven to be security attack lead through social engineering.

### Lessons Learned

This case highlights the importance of monitoring contributor activity,
especially in critical open source projects.

By using tools like Defected, maintainers can:
1. Proactively identify suspicious contributors.
2. Investigate anomalies in commit patterns.
3. Prevent security risks, such as backdoors, before they impact end users.

### Why This Matters

The case of **JiaT75** is a reminder that even trusted repositories can be
compromised. Open source maintainers need tools like Defected to protect their
projects from potential threats by identifying early warning signs such as
irregular timezone changes.

Obviously, not all timezone changes are suspicious, many of them are legit,
but like demonstrated by xz example some are real attempts. **JiaT75** tried
to show that he was located in Asia where some timezone changes reflect
western Europe timezone. Some timezone changes are so short that **JiaT75**
travel faster than light.

## How It Works

1. **Log Extraction**:
   - Extracts contributor metadata (author, email, date, timezone) using Git.
2. **Analysis**:
   - Groups commits by contributors.
   - Detects timezone changes and flags irregular patterns.
3. **Results**:
   - Outputs analysis to the terminal.
   - Exports results to a CSV file.

## Future Improvements

- **Holiday Detection**:
  - Cross-reference commit dates with public holiday calendars for anomaly
    detection.
- **Commit Pattern Visualization**:
  - Add heatmaps or graphs to visualize contributors' activity.
- **CI/CD Integration**:
  - Automate detection in pipelines to secure projects during updates.

## Contributing

We welcome contributions to Defected! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a detailed description of your changes.

## License

Defected is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

This project is inspired by the open source community and aims to empower
maintainers with tools to ensure project security and integrity.
