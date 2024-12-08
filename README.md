# GitHub Issue Transfer Tool

## Overview

This Python script is designed to transfer issues from multiple source repositories to a single destination repository on GitHub. It automates the process of migrating issues, preserving key details like titles, descriptions, and labels. This tool is useful for consolidating issues when managing multiple repositories.

## Features

- **Bulk Transfer**: Transfer issues from multiple repositories to a single destination repository.
- **Preserve Details**: Retains issue titles, bodies, and labels during the transfer.
- **Error Handling**: Provides clear feedback for failures during fetching or transferring issues.
- **Flexible Input**: Accepts source repositories via command-line arguments or from a text file.

## Requirements

Before using the script, ensure you have the following installed:

- **Python 3.x**: The script is compatible with Python 3.7 and higher.
- **Requests Library**: For making HTTP requests to interact with the GitHub API.

Install the required dependency with:

```bash
pip install requests
```

## Setup

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. GitHub API Token

You need a GitHub API token with the necessary permissions (e.g., repo scope). Create a token in your GitHub account under Settings > Developer settings > Personal access tokens.

### 3. Prepare Source Repositories

You can provide the source repositories in one of two ways:

* As Command-Line Arguments:

```
python transfer_issues.py -k <your-github-api-token> -s owner/repo1 owner/repo2 -d owner/destination-repo
```
* From a Text File:

Create a text file (source_repos.txt) with each repository on a new line:

```
owner/repo1
owner/repo2
```

Then run:

```
python transfer_issues.py -k <your-github-api-token> -f source_repos.txt -d owner/destination-repo
```

### 4. Running the Script

Execute the script with the appropriate arguments:

```
python transfer_issues.py -k <your-github-api-token> -s owner/repo1 owner/repo2 -d owner/destination-repo
```

## Command-Line Arguments

- `-k`, `--api-key`: **Required** – Your GitHub API token.  
- `-s`, `--source-repos`: List of source repositories (e.g., `owner/repo1 owner/repo2`).  
- `-f`, `--source-file`: Path to a text file containing source repository names (one per line).  
- `-d`, `--destination-repo`: **Required** – Destination repository (e.g., `owner/destination-repo`).  

## How It Works

- **Fetch Issues**: The script retrieves all issues (excluding pull requests) from the specified source repositories.  
- **Transfer Issues**: Each issue's title, body, and labels are used to create a new issue in the destination repository.  
- **Feedback**: The script provides detailed feedback on successful transfers or any errors encountered.  

## Example Usage

### Transferring Issues via Command-Line

```bash
python transfer_issues.py -k ghp_YourTokenHere -s user/repo1 user/repo2 -d user/destination-repo
```

## Transferring Issues via File Input

```bash
python transfer_issues.py -k ghp_YourTokenHere -f source_repos.txt -d user/destination-repo
```

## Example Output

```sql
Fetching issues from user/repo1...
Transferring issue 'Fix login bug' to user/destination-repo...
Successfully transferred issue: Fix login bug

Fetching issues from user/repo2...
Transferring issue 'Update documentation' to user/destination-repo...
Successfully transferred issue: Update documentation

Issue transfer complete
```
## Troubleshooting

- **Authentication Error**: Ensure your GitHub API token is valid and has the correct permissions.  
- **Invalid Repository**: Double-check the repository names (format: `owner/repo`).  
- **Rate Limiting**: GitHub API has rate limits; if you hit them, wait before retrying.  
- **File Not Found**: If using a file for source repositories, ensure the file path is correct.  
