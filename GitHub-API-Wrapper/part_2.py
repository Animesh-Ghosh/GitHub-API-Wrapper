'''Part 2 for the GitHub API wrapper.'''
import os
import time
from pprint import pprint
import requests
from dotenv import load_dotenv

# loading .env variables
load_dotenv()

# global constants
API = 'https://api.github.com'
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {os.environ["OAUTH_TOKEN"]}'
}
LANGUAGES = {'c++', 'python', 'scheme', '@formula'}


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
        # some error occured
        return res.json()['message']


if __name__ == '__main__':
    for lang in LANGUAGES:
        print(lang)
        repos = get_popular_repos(lang)
        pprint(repos)
