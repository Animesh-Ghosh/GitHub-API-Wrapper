'''Part 3 for the GitHub API.'''
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


def get_repo_top_contribs(repo_html_url):
    full_name = repo_html_url.split('https://github.com')[-1][1:]
    url = f'{API}/repos/{full_name}/contributors'
    print(url)
    res = requests.get(url=url, headers=HEADERS)
    # pprint(res.headers)

    # pprint(res.json())

    top_contribs = []
    for r in res.json()[:5]:
        # print(r['contributions'], r['html_url'])
        top_contribs.append({
            'contributor_html_url': r['html_url'],
            'contributions': r['contributions']
        })

    return top_contribs

if __name__ == '__main__':
    repo_html_url = input('Enter HTML URL of a repository: ')
    top_contribs = get_repo_top_contribs(repo_html_url)
    pprint(top_contribs)
