from githubapiclient import GitHubAPIClient
import json


if __name__ == "__main__":
    token = "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"  # Replace with your GitHub token
    repo_owner = "anomalous254"  # Replace with the repo owner's username

    client = GitHubAPIClient(token, repo_owner)

    # Example: Get commit data for a specific repository
    repo_name = "my-projects"
    result = client.fetch_repo_info(repo_name)
    print(json.dumps(result, indent=4))