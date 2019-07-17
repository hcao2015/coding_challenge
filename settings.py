GITHUB_API = 'https://api.github.com'
BITBUCKET_API = 'https://api.bitbucket.org/2.0'

GITHUB_PATHS = {
    'user_url': 'users/{user_name}',
    'repo_url': 'users/{user_name}/repos',
    'org_url': 'orgs/{organization_name}'
}

BITBUCKET_PATHS = {
    'user_url': 'users/{user_name}',
    'team_url': 'teams/{team_name}',
    'repo_url': 'repositories/{team_name}'
}
