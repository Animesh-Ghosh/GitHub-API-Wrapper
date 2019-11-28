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

# installing cache
requests_cache.install_cache(
    cache_name='github_api_wrapper_part_1_cache',
    backend='sqlite',
    expire_after=300
)


def get_public_repos():
    '''Returns the first 100 public repositories.'''
    url = f'{API}/repositories'
    return requests.get(url=url, headers=HEADERS)


def get_repo_star_count(repo):
    repo_url = repo['url']
    url = repo_url
    res = requests.get(url=url, headers=HEADERS)

    return res.json()['stargazers_count']


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


def get_repo_primary_lang(repo):
    repo_url = repo['url']
    url = f'{repo_url}/languages'

    res = requests.get(url=url, headers=HEADERS)

    languages = res.json()
    primary_lang = None
    line_count = 0

    for lang in languages:
        if languages[lang] > line_count:
            line_count = languages[lang]
            primary_lang = lang

    return primary_lang


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
    stargazers_count = get_repo_star_count(repo)
    primary_language = get_repo_primary_lang(repo)

    info = {
        'full_name': repo['full_name'],
        'html_url': repo['html_url'],
        'stargazers_count': stargazers_count,
        'contributors_count': contributors_count,
        'primary_language': primary_language,
        'open_pull_requests_count': open_pull_requests_count,
        'commits_count': commits_count
    }

    return info


if __name__ == '__main__':
    res = get_public_repos() # this needs to be called first
    # pprint(res.headers['Link'])
    # print('Number of public repositories returned:', len(res))
    repos = res.json()

    repos_info = []

    for repo in repos:
        repos_info.append(get_repo_info(repo))
        # break

    print('Repos sorted by number of open pull requests:')
    pprint(
        sorted(
            repos_info,
            key=lambda x: x['open_pull_requests_count'],
            reverse=True
        )[:10]
    )

    print('Repos sorted by number of commits:')
    pprint(
        sorted(
            repos_info,
            key=lambda x: x['commits_count'],
            reverse=True
        )[:10]
    )

    print('Repos sorted by number of contributors:')
    pprint(
        sorted(
            repos_info,
            key=lambda x: x['contributors_count'],
            reverse=True
        )[:10]
    )
