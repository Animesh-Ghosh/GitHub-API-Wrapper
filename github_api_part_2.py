'''Part 2 for the GitHub API.'''
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
LANGUAGES = {'c++', 'python', 'scheme'}


def get_popular_repos(lang):
	url = f'{API}/search/repositories?q=language:{lang}&sort=stars&order=desc'
	# print(url)
	return requests.get(url=url, headers=HEADERS)


if __name__ == '__main__':
	for lang in LANGUAGES:
		print(lang)
		res = get_popular_repos(lang)
		# print(len(res.json()['items']))
		for item in res.json()['items']:
			pprint(item['html_url'])
			# break
		# break
