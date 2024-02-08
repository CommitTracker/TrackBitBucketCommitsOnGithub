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
        response = requests.get(commits_url, headers=self._get_headers())
        if response.status_code == 200:
            data = response.json()
            commit_ids = [commit['hash'] for commit in data['values']] if not self.is_enterprise else [commit['id'] for commit in data['values']]
            return commit_ids
        else:
            return {"error": f"Failed to retrieve commits. Status code: {response.status_code}"}
