'''Part 1 for the GitHub API.'''
import os
import requests
from pprint import pprint
import time
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
    url = f'{API}/repositories'
    # print(url)
    return requests.get(url=url, headers=HEADERS)


def get_repo_star_count(repo):
    repo_url = repo['url']
    url = repo_url
    # print(url)
    res = requests.get(url=url, headers=HEADERS)

    return res.json()['stargazers_count']


def get_last_page_results(res):
    '''Returns the total number of items for paginated responses.'''
    # get number of pages and fetch last page results
    try:
        last_page_url = res.headers['Link'].split(',')[-1].strip().split(';')[0]\
                        .lstrip('<').rstrip('>')
        num_pages = last_page_url.split('?')[-1].split('=')[-1]
        # print(last_page_url)
        # print(num_pages)

        last_page_res = requests.get(url=last_page_url, headers=HEADERS)

        # number of pages - 1 (1 for the last page) * number of items per page + number of results from last page
        return (int(num_pages) - 1) * NUM_ITEMS_PER_PAGE + len(last_page_res.json())

    except KeyError:
        # no 'Link' header, only one page
        return len(res.json())


def get_repo_contrib_count(repo):
    repo_url = repo['url']
    url = f'{repo_url}/contributors'
    # print(url)
    res = requests.get(url=url, headers=HEADERS)

    # pprint(res.headers)
    return get_last_page_results(res)


def get_repo_primary_lang(repo):
    repo_url = repo['url']
    url = f'{repo_url}/languages'
    # print(url)
    res = requests.get(url=url, headers=HEADERS)

    languages = res.json()
    primary_lang = None
    line_count = 0

    for lang in languages:
        if languages[lang] > line_count:
            line_count = languages[lang]
            primary_lang = lang

    return primary_lang


def get_repo_info(repo):
    '''Get the repo info including number of stars, number of contributors and

    the primary language used.
    '''
    star_count = get_repo_star_count(repo)
    contributor_count = get_repo_contrib_count(repo)
    primary_language = get_repo_primary_lang(repo)

    info = {
        'repo_url': repo['html_url'],
        'star_count': star_count,
        'contrib_count': contributor_count,
        'primary_lang': primary_language
    }

    return info


def get_repo_open_pulls(repo):
    repo_url = repo['url']
    url = f'{repo_url}/pulls?state=open'
    res = requests.get(url=url, headers=HEADERS)

    return get_last_page_results(res)


def get_repo_commits(repo):
    repo_url = repo['url']
    url = f'{repo_url}/commits'
    res = requests.get(url=url, headers=HEADERS)

    return get_last_page_results(res)


if __name__ == '__main__':
    res = get_public_repos()
    # pprint(res.headers)
    repos = res.json()
    # pprint(repos)
    # print(len(repos))
    for repo in repos:
        # pprint(repo)
        print("Repo info:")
        pprint(get_repo_info(repo))
        print("Commits in repo: ", get_repo_commits(repo))
        print("Open pull requests:", get_repo_open_pulls(repo))
        break
