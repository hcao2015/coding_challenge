# Coding Challenge App

A skeleton flask app to use for a coding challenge.

## Install:

You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.yml
source activate user-profiles
```

Or just pip install from the requirements file
``` 
pip install -r requirements.txt
```

## Running the code

### Spin up the service

```
# start up local server
python -m run 
```

### Making Requests

```
curl -i "http://127.0.0.1:5000/health-check"
curl -i "http://127.0.0.1:5000/api/v1/teams/{team_name}"
curl -i "http://127.0.0.1:5000/api/v1/orgs/{org_name}/teams/{team_name}"
```
Example:
```
curl -i http://127.0.0.1:5000/api/v1/teams/pygame
curl -i http://127.0.0.1:5000/api/v1/orgs/mailchimp/teams/pygame
```
It will return team profile with sample:
```
 "data": {
    "followers_count": 0, 
    "forked_repos_count": 0, 
    "list_languages": {}, 
    "original_repos_count": 0, 
    "public_repos_count": 0, 
    "repos": {
        "repo_name": {
            "description": "", 
            "forks_count": 0, 
            "language": "", 
            "watchers_count": 0
      }
    }
```

### Run tests
```
python -m unittest
```
## What'd I'd like to improve on...
I'd like to try GraphQL to compare its efficiency versus regular Api