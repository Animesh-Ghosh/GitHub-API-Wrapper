from flask import Flask, render_template
from flask_restful import Resource, Api
import requests_cache
from github_api_wrapper_part_1 import (
    get_public_repos, get_repo_info
)
from github_api_wrapper_part_2 import get_popular_repos
from github_api_wrapper_part_3 import get_repo_top_contribs

app = Flask(__name__)
api = Api(app)

# installing cache
requests_cache.install_cache(
    cache_name='github_api_wrapper_cache',
    backend='sqlite',
    expire_after=600
)


def long_reqs():
    '''Runs before the first request to the server if cache doesn't exist,
    thus making server startup slow. Needed so that site can perform better,
    however, when the cache expires, the request will again become slow, since

    getting info for each repo takes a while.
    '''
    print('Getting public repos.')
    repos = get_public_repos()

    print('Getting info for repos.')
    for repo in repos:
        get_repo_info(repo)

    print('Done.')


class Repos(Resource):
    '''Part 1.'''
    def get(self, filter):
        # remove expired responses
        requests_cache.remove_expired_responses()

        repos_info = []
        repos = get_public_repos()

        for repo in repos:
            # will be slow if cache doesn't exist yet or has expired
            repos_info.append(get_repo_info(repo))

        if filter == 'prs':
            result = sorted(
                repos_info,
                key=lambda x: x['open_pull_requests_count'],
                reverse=True
            )
            return {'repositories': result}

        elif filter == 'commits':
            result = sorted(
                repos_info,
                key=lambda x: x['commits_count'],
                reverse=True
            )
            return {'repositories': result}

        elif filter == 'contribs':
            result = sorted(
                repos_info,
                key=lambda x: x['contributors_count'],
                reverse=True
            )
            return {'repositories': result}

        return {'fault': 'Invalid filter.'}


class PopularRepos(Resource):
    '''Part 2.'''
    def get(self, lang):
        # remove expired responses
        requests_cache.remove_expired_responses()

        repos = get_popular_repos(lang)

        return {'popular_repositories': repos}


class TopRepoContribs(Resource):
    '''Part 3.'''
    def get(self, repo_html_url):
        # remove expired responses
        requests_cache.remove_expired_responses()

        repo_full_name, top_contribs = get_repo_top_contribs(repo_html_url)

        return {'top_contributors': top_contribs}


api.add_resource(
    Repos,
    '/api/repos/filter/<string:filter>',
    endpoint='repos-by-filter'
)
api.add_resource(
    PopularRepos,
    '/api/repos/<string:lang>',
    endpoint='repos-by-lang'
)
api.add_resource(
    TopRepoContribs,
    '/api/repos/<path:repo_html_url>/top-contribs',
    endpoint='top-contribs'
)


app.before_first_request(long_reqs)


@app.route('/')
def index():
    return render_template('index.html')
