'''Part 2 for the GitHub API wrapper.'''
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
LANGUAGES = {'c++', 'python', 'scheme'}


def get_popular_repos(lang):
    '''Returns the most popular repositories for a specified language.
    
    Returns 30 results according to the default page size of GitHub's API.
    '''
    repos = []
    url = f'{API}/search/repositories?q=language:{lang}&sort=stars&order=desc'

    res = requests.get(url=url, headers=HEADERS)

    for item in res.json()['items']:
        repos.append({
            'full_name': item['full_name'],
            'html_url': item['html_url'],
            'language': item['language'],
            'stargazers_count': item['stargazers_count']
        })

    return repos


if __name__ == '__main__':
    for lang in LANGUAGES:
        print(lang)
        repos = get_popular_repos(lang)
        pprint(repos)
