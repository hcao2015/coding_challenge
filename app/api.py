import requests
import logging
import settings
import json

logger = logging.getLogger('app.api')

class BaseAPI(object):
    def __init__(self, **kwargs):
        self.organization_name = kwargs.get('organization_name')
        self.team_name = kwargs.get('team_name')
        self.access_token = kwargs.get('access_token')

    @staticmethod
    def _make_request(url):
        try:
            response = requests.get(url)
            logger.info(f"Starting a request to {url}")
            if response.status_code == 200:
                return json.loads(response.content)
            logger.error(f'Error: Request to {url} return {response.status_code}')
        except Exception:
            pass

        return {}


class ApiResult(object):
    """
    It's used to format output data
    """
    NOT_FOUND = 'Not Found'
    ERROR = 'error'
    SUCCESS = 'success'
    WARNING = 'warning'

    def __init__(self, result=None, data=None, error_title=None, error_message=None):
        self.result = result
        self.data = data
        self.error_title = error_title
        self.error_message = error_message

    def to_format(self):
        if self.result == ApiResult.ERROR:
            return {
                'data': {
                    'error': {
                        'title': self.error_title,
                        'message': self.error_message
                    }
                },
                'status': 404
            }
        return {
            'data': self.data,
            'status': 200
        }


class MainAPI(BaseAPI):

    def _extract_and_merge_data(self, git_user_data, git_repos_data, bitbucket_repos_data):
        output_repo = {}
        list_languages = {}

        # Extract count of public repos and followers from Github
        public_repos_count = git_user_data.get('public_repos', 0)
        followers_count = git_user_data.get('followers', 0)
        fork_repos_count = 0

        logger.info(f'Github account {self.team_name} returns:'
                    f'public_repos = {public_repos_count}, followers_count = {followers_count}')

        # Extract these attributes from each github repo
        github_attrs = ['fork', 'forks_count', 'watchers_count', 'language', 'description']
        for repo in git_repos_data:
            repo_data = {}
            for attr in github_attrs:

                # Detect if the repo is original or forked
                if attr == 'fork':
                    if repo[attr]:
                        fork_repos_count += 1
                else:
                    repo_data[attr] = repo.get(attr, None)

                    # Count languages
                    if attr == 'language' and repo[attr]:
                        lang = repo[attr].lower()
                        if lang in list_languages:
                            list_languages[lang] += 1
                        else:
                            list_languages[lang] = 1

            output_repo[repo['name']] = repo_data

        # Extract these attributes from each repo of Bitbucket
        if len(bitbucket_repos_data) > 0:
            bitbucket_attrs = ['is_private', 'language', 'description']
            for repo in bitbucket_repos_data:
                repo_data = dict()
                repo_data['watchers_count'] = 0
                if repo['name'] not in output_repo:
                    for attr in bitbucket_attrs:

                        # Detect if the repo is public or private
                        if attr == 'is_private':
                            if not repo[attr]:
                                public_repos_count += 1
                        else:
                            repo_data[attr] = repo.get(attr, None)

                            if attr == 'language' and repo[attr]:
                                lang = repo[attr].lower()
                                if lang in list_languages:
                                    list_languages[lang] += 1
                                else:
                                    list_languages[lang] = 1
                    # get count of watchers
                    try:
                        repo_url = repo['links']['watchers']['href']
                        repo_data['watchers_count'] += self._make_request(repo_url)['size']
                    except KeyError:
                        pass
                    output_repo[repo['name']] = repo_data

        output_data = {
            'public_repos_count': public_repos_count,
            'followers_count': followers_count,
            'forked_repos_count': fork_repos_count,
            'original_repos_count': public_repos_count - fork_repos_count,
            'list_languages': list_languages,
            'repos': output_repo
        }
        logger.info(f'Merged data of Github and Bitbucket: {output_data}')
        return ApiResult(result=ApiResult.SUCCESS, data=output_data).to_format()

    def get_individual_team(self):
        """
        It provides a merged team profile between Github and Bitbucket
        :return:
        """
        git_url = f"{settings.GITHUB_API}/{settings.GITHUB_PATHS['user_url'].format(user_name=self.team_name)}"
        git_user_data = self._make_request(git_url)

        bitbucket_repos_url = f"{settings.BITBUCKET_API}/" \
                              f"{settings.BITBUCKET_PATHS['repo_url'].format(team_name=self.team_name)}"
        bitbucket_repos_data = self._make_request(bitbucket_repos_url).get('values', [])
        if not git_user_data:
            return ApiResult(result=ApiResult.ERROR, error_title=ApiResult.NOT_FOUND,
                             error_message='Unable to get the team name info from Github').to_format()
        git_repos_data = self._make_request(git_user_data['repos_url'])

        return self._extract_and_merge_data(git_user_data, git_repos_data, bitbucket_repos_data)

    def get_team_in_org_info(self):
        """
        It provides way for a client to provide the Github organization and Bitbucket team
        names to merge for the profile
        :return:
        """
        org_path = settings.GITHUB_PATHS['org_url'].format(organization_name=self.organization_name)
        git_url = f"{settings.GITHUB_API}/{org_path}"

        git_data = self._make_request(git_url)

        if not git_data:
            return ApiResult(result=ApiResult.ERROR, error_title=ApiResult.NOT_FOUND,
                             error_message='Unable to get the org info from Github').to_format()
        repos_url = git_data.get('repos_url', None)

        git_repos_data = self._make_request(repos_url)

        bitbucket_repos_url = f"{settings.BITBUCKET_API}/" \
                              f"{settings.BITBUCKET_PATHS['repo_url'].format(team_name=self.team_name)}"
        bitbucket_repos_data = self._make_request(bitbucket_repos_url).get('values', [])

        return self._extract_and_merge_data(git_data, git_repos_data, bitbucket_repos_data)

