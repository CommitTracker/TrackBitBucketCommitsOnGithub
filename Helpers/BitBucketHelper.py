import requests

class BitBucketHelper:
    def __init__(self, data):
        self.username = data["Username"]
        self.app_password = data["AppPassword"]
        self.workspace = data["Workspace"]
        self.repo = data["Repo"]
        self.is_premium = data["isPremium"]
        self.is_enterprise = data["isEnterprise"]
        self.enterprise_url = data["enterpriseUrl"] if self.is_enterprise else None
        
        if self.is_enterprise:
            self.base_url = f"{self.enterprise_url}/rest/api/1.0/projects/{self.workspace}/repos/{self.repo}"
        elif self.is_premium:
            self.base_url = f"https://api.bitbucket.org/premium/2.0/repositories/{self.workspace}/{self.repo}"
        else:
            self.base_url = f"https://api.bitbucket.org/2.0/repositories/{self.workspace}/{self.repo}"

    def _get_headers(self):
        if self.is_enterprise:
            headers = {'Authorization': f'Bearer {self.app_password}'}
        else:
            auth = requests.auth.HTTPBasicAuth(self.username, self.app_password)
            headers = {'Authorization': 'Basic ' + auth}
        return headers

    def get_all_commit_data(self):
        commits_url = f"{self.base_url}/commits"
        params = {'pagelen': 100}  # Adjust based on API limits
        all_commits = []

        while len(all_commits) < 250:
            response = requests.get(commits_url, headers=self._get_headers(), params=params)
            if response.status_code == 200:
                data = response.json()
                # For non-enterprise, filter commits by author username
                if not self.is_enterprise:
                    for commit in data['values']:
                        if 'author' in commit and 'user' in commit['author'] and commit['author']['user']['username'] == self.username:
                            all_commits.append(commit['hash'])
                            if len(all_commits) >= 250:
                                break
                # For enterprise, adjust accordingly based on your enterprise API structure
                else:
                    for commit in data['values']:
                        # Assuming enterprise version has a similar structure, adjust as necessary
                        if commit['author']['slug'] == self.username:  # Adjust the condition based on actual API response structure
                            all_commits.append(commit['id'])
                            if len(all_commits) >= 250:
                                break
                # Check if there's a next page, otherwise break
                if 'next' in data:
                    commits_url = data['next']  # Update the URL to the next page of commits
                else:
                    break
            else:
                return {"error": f"Failed to retrieve commits. Status code: {response.status_code}"}

        return all_commits[:250]  # Ensure to return only up to 250 commits

