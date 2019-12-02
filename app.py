from datetime import timedelta
from flask import Flask, render_template
from flask_restful import abort, Api, Resource
import requests
import requests_cache
from core import (
    API, HEADERS,
    get_repos_info_multi_threading,
    get_popular_repos,
    get_repo_top_contribs
)

app = Flask(__name__)
api = Api(
    app,
    default_mediatype='application/json',
    catch_all_404s=True,
)

# installing cache
requests_cache.install_cache(
    cache_name='github_api_wrapper_cache',
    backend='sqlite',
    expire_after=timedelta(minutes=10)
)


class Repos(Resource):
    '''Part 1.'''
    def get(self, filter):
        # remove expired responses
        requests_cache.remove_expired_responses()

        repos_info = get_repos_info_multi_threading()

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

        try:
            repos = get_popular_repos(lang)

            if len(repos[0]) == 1:
                raise ValueError()

            return {
                'response': {
                    'popular_repositories': repos
                }
            }

        except ValueError:
            # language doesn't exists in GitHub's database or query invalid
            message = get_popular_repos(lang)
            return {
                'response': {
                    'message': message
                }
            }



class TopRepoContribs(Resource):
    '''Part 3.'''
    def get(self, repo_html_url):
        # remove expired responses
        requests_cache.remove_expired_responses()

        try:
            repo_full_name, top_contribs = get_repo_top_contribs(repo_html_url)
            return {
                'response': {
                    'full_name': repo_full_name,
                    'top_contributors': top_contribs
                }
            }

        except ValueError:
            # contributor list too large
            message = get_repo_top_contribs(repo_html_url)
            return {
                'response': {
                    'message': message
                }
            }


api.add_resource(
    Repos,
    '/api/v1/repos/filter/<string:filter>',
    endpoint='repos-by-filter'
)
api.add_resource(
    PopularRepos,
    '/api/v1/repos/popular/<path:lang>',
    endpoint='repos-by-lang'
)
api.add_resource(
    TopRepoContribs,
    '/api/v1/repos/<path:repo_html_url>/top-contribs',
    endpoint='top-contribs'
)


@app.route('/')
def index():
    res = requests.get(API, headers=HEADERS)
    requests_remaining = res.headers['X-RateLimit-Remaining'] # GitHub API's remaining requests

    return render_template('index.html',requests_remaining=requests_remaining)


@app.route('/api')
def api_index():
    return render_template('api.html', title=' - Documentation')
