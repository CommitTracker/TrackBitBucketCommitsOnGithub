from Helpers.BitBucketHelper import BitBucketHelper
from Helpers.GithubHelper import GithubHelper
from Helpers.JsonHelper import JsonHelper
import time

def main():
    JsHelper = JsonHelper()
    apps_data = JsHelper.GetData()
    try:
        # Initialize helpers
        for data in apps_data:
            bitbucket_helper = BitBucketHelper(data)
            github_helper = GithubHelper()

            # Get all commit data from Bitbucket
            bitbucket_commits = bitbucket_helper.get_all_commit_data()
            if isinstance(bitbucket_commits, dict) and 'error' in bitbucket_commits:
                print(f"Error fetching Bitbucket commits: {bitbucket_commits['error']}")
                continue

            # List files in the 'commits' directory on GitHub
            github_commits = github_helper.list_files_in_dir("commits")
            if not github_commits:  # Checks if github_commits is empty or an error occurred
                print("Error or no files found in GitHub 'commits' directory.")
                continue

            # Convert lists to sets for comparison
            bitbucket_commits_set = set(bitbucket_commits)
            github_commits_set = set(github_commits)

            # Find commits new to Bitbucket
            new_to_bitbucket = bitbucket_commits_set - github_commits_set
            if not new_to_bitbucket:
                print("No new commits in Bitbucket to update to GitHub.")
                continue

            print(f"{len(new_to_bitbucket)} commits to push.")

            for commit in new_to_bitbucket:
                # Try to commit each new commit to GitHub
                try:
                    # Assuming the commit message or content is being fetched in a manner suitable for GitHub
                    commit_message = f"Commit {commit} from Bitbucket"
                    github_helper.commit(commit_message, "commits", f"{commit}.txt", file_content="Commit details here")
                except Exception as e:
                    print(f"Failed to commit {commit} to GitHub: {e}")

            print("Process completed successfully.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
