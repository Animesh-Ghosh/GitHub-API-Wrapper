'''Part 3 for the GitHub API wrapper.'''
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

# installing cache
requests_cache.install_cache(
    cache_name='github_api_wrapper_part_3_cache',
    backend='sqlite',
    expire_after=300
)


def get_repo_top_contribs(repo_html_url):
    '''Returns the top 5 contributors for the repository specified by the repository's
    GitHub link.
    '''
    top_contribs = []
    full_name = repo_html_url.split('https://github.com')[-1][1:]
    url = f'{API}/repos/{full_name}/contributors'

    res = requests.get(url=url, headers=HEADERS)

    for r in res.json()[:5]:
        top_contribs.append({
            'html_url': r['html_url'],
            'contributions': r['contributions']
        })

    return top_contribs


if __name__ == '__main__':
    repo_html_url = input('Enter HTML URL of a repository: ')
    top_contribs = get_repo_top_contribs(repo_html_url)
    pprint(top_contribs)
