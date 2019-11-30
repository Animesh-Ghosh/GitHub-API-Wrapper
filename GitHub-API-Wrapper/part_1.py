'''Part 1 for the GitHub API wrapper.'''
import os
import time
from pprint import pprint
import requests
import requests_cache
from dotenv import load_dotenv

# loading .env variables
load_dotenv()
OAUTH_TOKEN = os.environ['OAUTH_TOKEN']

# global constants
API = 'https://api.github.com'
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {OAUTH_TOKEN}'
}
NUM_ITEMS_PER_PAGE = 30


def get_public_repos():
    '''Returns popular public repos sorted by number of stars.'''
    repos = []
    url = f'{API}/search/repositories?q=is:public&sort=stars&order=desc'

    res = requests.get(url=url, headers=HEADERS)

    for item in res.json()['items']:
        repos.append({
            'full_name': item['full_name'],
            'html_url': item['html_url'],
            'url': item['url'], # api url
            'language': item['language'],
            'stargazers_count': item['stargazers_count']
        })

    return repos


def get_last_page_results(res):
    '''Returns the total number of items for paginated responses.'''
    # get number of pages and fetch last page results
    try:
        last_page_url = res.links['last']['url']
        num_pages = last_page_url.split('?')[-1].split('=')[-1]

        last_page_res = requests.get(url=last_page_url, headers=HEADERS)

        # number of pages - 1 (1 for the last page) * number of items per page + number of results from last page
        return (int(num_pages) - 1) * NUM_ITEMS_PER_PAGE + len(last_page_res.json())

    except KeyError:
        # no 'Link' header, only one page
        return len(res.json())


def get_repo_contrib_count(repo):
    repo_url = repo['url']
    url = f'{repo_url}/contributors'

    res = requests.get(url=url, headers=HEADERS)

    return get_last_page_results(res)


def get_repo_open_pulls_count(repo):
    repo_url = repo['url']
    url = f'{repo_url}/pulls?state=open'
    res = requests.get(url=url, headers=HEADERS)

    return get_last_page_results(res)


def get_repo_commits_count(repo):
    repo_url = repo['url']
    url = f'{repo_url}/commits'
    res = requests.get(url=url, headers=HEADERS)

    return get_last_page_results(res)


def get_repo_info(repo):
    '''Get the repo info including number of stars, number of contributors and the
    primary language used.
    '''
    open_pull_requests_count = get_repo_open_pulls_count(repo)
    commits_count = get_repo_commits_count(repo)
    contributors_count = get_repo_contrib_count(repo)

    info = {
        'full_name': repo['full_name'],
        'html_url': repo['html_url'],
        'stargazers_count': repo['stargazers_count'],
        'language': repo['language'],
        'contributors_count': contributors_count,
        'open_pull_requests_count': open_pull_requests_count,
        'commits_count': commits_count
    }

    return info


if __name__ == '__main__':
    repos = get_public_repos()

    repos_info = []

    for repo in repos:
        repos_info.append(get_repo_info(repo))

    print('Repos sorted by number of open pull requests:')
    pprint(
        sorted(
            repos_info,
            key=lambda x: x['open_pull_requests_count'],
            reverse=True
        )[:5]
    )

    print('Repos sorted by number of commits:')
    pprint(
        sorted(
            repos_info,
            key=lambda x: x['commits_count'],
            reverse=True
        )[:5]
    )

    print('Repos sorted by number of contributors:')
    pprint(
        sorted(
            repos_info,
            key=lambda x: x['contributors_count'],
            reverse=True
        )[:5]
    )
