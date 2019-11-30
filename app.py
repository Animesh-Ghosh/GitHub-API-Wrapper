from flask import Flask, render_template
from flask_restful import abort, Api, Resource
import requests_cache
from core import (
    get_public_repos, get_repo_info,
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
    # expire_after=600 # persisting forever temporarily
)


def long_reqs():
    '''Runs before the first request to the server. Needed so that site can
    perform better. If cache doesn't exist, server startup is slow. However, when
    the cache expires, the request will again become slow, since getting info for

    each repo takes a while.
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
        print('Getting public repos.')
        repos = get_public_repos()

        print('Getting info for repos.')
        for repo in repos:
            # will be slow if cache doesn't exist yet or has expired
            repos_info.append(get_repo_info(repo))

        print('Done.')

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
    '/api/v1/repos/popular/<string:lang>',
    endpoint='repos-by-lang'
)
api.add_resource(
    TopRepoContribs,
    '/api/v1/repos/<path:repo_html_url>/top-contribs',
    endpoint='top-contribs'
)

app.before_first_request(long_reqs)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api')
def api_index():
    return render_template('api.html', title=' - Documentation')
