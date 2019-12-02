import os
import time
from pprint import pprint
from concurrent import futures
import requests
import requests_cache
from dotenv import load_dotenv

# loading .env variables
load_dotenv()

# global constants
API = 'https://api.github.com'
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {os.environ["OAUTH_TOKEN"]}'
}
NUM_ITEMS_PER_PAGE = 30

# part 1 begin


def get_public_repos():
    '''Returns popular public repos sorted by number of stars.'''
    print('Getting public repos.')

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
        print('Getting last page results.')
        num_pages = last_page_url.split('?')[-1].split('=')[-1]

        last_page_res = requests.get(url=last_page_url, headers=HEADERS)

        # number of pages - 1 (1 for the last page) * number of items per page +
        # number of results from last page
        return (int(num_pages) - 1) * NUM_ITEMS_PER_PAGE + len(last_page_res.json())

    except KeyError:
        # no 'Link' header, only one page
        print('No last page.')
        return len(res.json())


def get_repo_contrib_count(repo):
    print('Getting contributors count.')

    url = f'{repo["url"]}/contributors'
    res = requests.get(url=url, headers=HEADERS)

    return get_last_page_results(res)


def get_repo_open_pulls_count(repo):
    print('Getting pull requests count.')

    url = f'{repo["url"]}/pulls?state=open'
    res = requests.get(url=url, headers=HEADERS)

    return get_last_page_results(res)


def get_repo_commits_count(repo):
    print('Getting commits count.')

    url = f'{repo["url"]}/commits'
    res = requests.get(url=url, headers=HEADERS)

    return get_last_page_results(res)


def get_repo_info(repo):
    '''Get the repo info including number of stars, number of contributors and the
    primary language used.
    '''
    print(f'Getting info for {repo["full_name"]}.')

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


def get_repos_info_multi_threading():
    '''Returns the repos info in bulk using multi-threading.

    Fastest, since networking requests are I/O.
    '''
    with futures.ThreadPoolExecutor() as executor:
        repos = get_public_repos()
        results = executor.map(get_repo_info, repos)

        repos_info = []

        for result in results:
            repos_info.append(result)

    return repos_info


# part 1 end
# part 2 begin


def url_escaped_lang(lang):
    '''Converts the language into URI escaped language for making queries.'''
    url_escape_chars = {
        ' ': '%20', '#': '%23',
        '@': '%40', '/': r'%2F',
        ':': '%3A',  '+': '%2B'
    }

    for char in lang:
        if char in url_escape_chars:
            lang = lang.replace(char, url_escape_chars[char])

    return lang


def get_popular_repos(lang):
    '''Returns the most popular repositories for a specified language.
    
    Returns 30 results according to the default page size of GitHub's API.
    '''
    repos = []
    lang = url_escaped_lang(lang)
    print(f'URL escaped language: {lang}')
    url = f'{API}/search/repositories?q=language:{lang}&sort=stars&order=desc'

    res = requests.get(url=url, headers=HEADERS)

    try:
        # if language exists in GitHub's database
        for item in res.json()['items']:
            repos.append({
                'full_name': item['full_name'],
                'html_url': item['html_url'],
                'language': item['language'],
                'stargazers_count': item['stargazers_count']
            })

        return repos

    except KeyError:
        # language doesn't exists in GitHub's database or query invalid
        return res.json()['message']


# part 2 end
# part 3 begin


def get_repo_top_contribs(repo_html_url):
    '''Returns the top 5 contributors for the repository specified by the repository's
    
    GitHub link.
    '''
    top_contribs = []
    full_name = repo_html_url.split('https://github.com/')[-1]
    url = f'{API}/repos/{full_name}/contributors'

    res = requests.get(url=url, headers=HEADERS)

    try:
        for r in res.json()[:5]:
            top_contribs.append({
                'login': r['login'],
                'html_url': r['html_url'],
                'avatar_url': r['avatar_url'],
                'contributions': r['contributions']
            })

        return (full_name, top_contribs)

    except TypeError:
        # contributor list too large
        return res.json()['message']


# part 3 end
