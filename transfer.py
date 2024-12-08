import requests
import json

# GitHub API Base URL
GITHUB_API_URL = "https://api.github.com"

def transfer_issues(api_key, source_repos, destination_repo):
    """
    Transfers issues from multiple source repositories to a destination repository.

    Args:
        api_key (str): GitHub API token with necessary permissions.
        source_repos (list): List of source repositories in 'owner/repo' format.
        destination_repo (str): Destination repository in 'owner/repo' format.
    """
    # Set headers for authentication and API request
    headers = {
        "Authorization": f"token {api_key}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Iterate through each source repository
    for source_repo in source_repos:
        print(f"\nFetching issues from {source_repo}...")
        
        # Fetch issues from the source repository
        response = requests.get(f"{GITHUB_API_URL}/repos/{source_repo}/issues", headers=headers)

        # Handle errors in fetching issues
        if response.status_code != 200:
            print(f"Failed to fetch issues from {source_repo}. Error: {response.json()}")
            continue

        # Parse the response JSON into a list of issues
        issues = response.json()
        for issue in issues:
            # Skip pull requests as they are not standard issues
            if 'pull_request' in issue:
                continue

            # Prepare the issue data for transfer
            issue_data = {
                "title": issue["title"],  # Issue title
                "body": issue["body"],  # Issue description or body
                "labels": [label["name"] for label in issue.get("labels", [])],  # Issue labels
            }

            # Transfer the issue to the destination repository
            print(f"Transferring issue '{issue['title']}' to {destination_repo}...")
            create_response = requests.post(
                f"{GITHUB_API_URL}/repos/{destination_repo}/issues",
                headers=headers, 
                json=issue_data
            )

            # Handle success or failure of the transfer
            if create_response.status_code == 201:
                print(f"Successfully transferred issue: {issue['title']}")
            else:
                print(f"Failed to transfer issue '{issue['title']}'. Error: {create_response.json()}")

    print("\nIssue transfer complete")

def load_source_repos_from_file(file_path):
    """
    Reads a list of source repositories from a text file.

    Args:
        file_path (str): Path to the text file containing repository names.

    Returns:
        list: List of repository names in 'owner/repo' format, or an empty list if the file is not found.
    """
    try:
        # Open the file and read each line, stripping whitespace
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        # Handle missing file error
        print(f"Error: File '{file_path}' not found.")
        return []

# Main entry point for the script
if __name__ == "__main__":
    import argparse

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Transfer GitHub issues from multiple repositories to a destination repository.")
    parser.add_argument("-k", "--api-key", required=True, help="GitHub API token with repository access.")
    parser.add_argument("-s", "--source-repos", nargs="*", help="List of source repositories in 'owner/repo' format.")
    parser.add_argument("-f", "--source-file", help="File containing source repositories (one per line).")
    parser.add_argument("-d", "--destination-repo", required=True, help="Destination repository in 'owner/repo' format.")

    # Parse command-line arguments
    args = parser.parse_args()

    # Ensure at least one source repository is provided
    if not args.source_repos and not args.source_file:
        print("Error: You must provide either a list of source repositories or a file containing repositories.")
        exit(1)

    # Load the list of source repositories from arguments or file
    source_repos = args.source_repos or load_source_repos_from_file(args.source_file)
    if not source_repos:
        print("No source repositories provided.")
        exit(1)

    # Transfer issues from source repositories to the destination repository
    transfer_issues(args.api_key, source_repos, args.destination_repo)
