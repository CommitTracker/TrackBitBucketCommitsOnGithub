import requests

class BitBucketHelper:
    def __init__(self, data):
        self.username = data["Username"]
        self.app_password = data["AppPassword"]
        self.workspace = data["Workspace"]
        self.repo_slug = data["Repo"]
        self.base_url = f"https://api.bitbucket.org/2.0/repositories/{self.workspace}/{self.repo_slug}"

    def _get_headers(self):
        """Prepare authorization headers with Basic Auth using app password."""
        auth = requests.auth.HTTPBasicAuth(self.username, self.app_password)
        return auth

    def get_all_commit_data(self):
        commits_url = f"{self.base_url}/commits/"
        response = requests.get(commits_url, auth=self._get_headers())
        if response.status_code == 200:
            data = response.json()
            commit_ids = [commit['hash'] for commit in data['values']]
            return commit_ids  # Return a list of commit hashes
        else:
            return {"error": f"Failed to retrieve commits. Status code: {response.status_code}"}
