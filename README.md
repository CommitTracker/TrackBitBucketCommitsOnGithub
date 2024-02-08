# Track BitBucket Commits on Github

**_Description_**

This checks for any pushes to a repo in BitBucket and then creates commits in a GitHub repo.

**_Pre Requisites_**

This was created with [Python Version 3.11.7](https://www.python.org/downloads/release/python-3117).  
Make sure you have GitPython installed `pip install GitPython`.  
Create an App Password in BitBucket: [App Password](https://bitbucket.org/account/settings/app-passwords/).  
Make sure to give the App Password **Repository Read** access.

**_How To Use_**

- Use the template to create a new private repository
- Clone that repository to the local machine
- Open app settings and update it with relevant information: `(https://bitbucket.org/{yourWorkspace}/{yourRepo})`
- If you are having package issues run the [`installer.bat`](https://github.com/illuminat3/TrackBitBucketCommitsOnGithub/blob/main/installer.bat) script.


