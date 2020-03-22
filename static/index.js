// using strict mode
'use strict';

// defining global constant APIRoot
const APIRoot = `${window.origin}/api/v1`;

// registering Vue components
Vue.component('filtered-repository', {
	props: ['repository'],
	template : `<li style="padding-bottom: 10px;">
	<a v-bind:href="repository['html_url']">
		{{ repository['full_name'] }}
	</a><br>
	Stars: {{ repository['stargazers_count'] }}<br>
	Language: {{ repository['language'] }}<br>
	Contributors: {{ repository['contributors_count'] }}<br>
	Open Pull Requests: {{ repository['open_pull_requests_count'] }}<br>
	Commits: {{ repository['commits_count'] }}<br>
	Contributors: {{ repository['contributors_count'] }}
</li>`,
});
Vue.component('popular-repository', {
	props: ['repository'],
	template : `<li style="padding-bottom: 10px;">
	<a v-bind:href="repository['html_url']">
		{{ repository['full_name'] }}
	</a><br>
  Stars: {{ repository['stargazers_count'] }}
</li>`,
});
Vue.component('contributor', {
	props : ['contributor'],
	template : `<li style="padding-bottom: 15px;">
	<a v-bind:href="contributor['html_url']">
		{{ contributor['login'] }}
	</a><br>
	<img v-bind:src="contributor['avatar_url']"><br>
	Contributions: {{ contributor['contributions'] }}
</li>`,
});

// creating Vue instance
let app = new Vue({
	el : '#app',
	data : {
		// data for number of API requests remaining
		ratelimitRemaining: false,
		requestsRemaining: 0,

		// data for getting repos by filter
		filteredRepos : false,
		selected : 'prs',
		options : [
			{ text : 'Open Pull Requests', value : 'prs' },
			{ text : 'Number of Commits', value : 'commits' },
			{ text : 'Number of Contributors', value : 'contribs' },
		],

		// data for getting repos by language
		popularRepos : false,
		repoLanguage : '',

		// data for getting repo contributors
		contributors : false,
		repoURL : '',

		// data for showing message and rendering results
		message : '',
		results : [],
	},
	methods : {
		// function to update the number of remaining requests
		getRequestsRemainingVue : async function() {
			const response = await fetch(
				`${APIRoot}/requests-remaining`, {
					mode : 'same-origin',
					cache : 'no-cache'
				}
			);
			const JSONResponse = await response.json();
			// console.log(JSONResponse);

			this.requestsRemaining = window.parseInt(JSONResponse['response']['ratelimit_remaining'], 10);
			this.ratelimitRemaining = true;
		},
		//
		getFilteredReposVue : async function(event) {
			// setting flags to render only filtered-repository component
			this.filteredRepos = true;
			this.popularRepos = !this.filteredRepos;
			this.contributors = !this.filteredRepos;

			this.message = 'Please wait while the server processes your request...';
			this.results = [];

			const response = await fetch(
				`${APIRoot}/repos/filter/${this.selected}`, {
					cache : 'default',
				}
			);
			const JSONResponse = await response.json();
			// console.log(JSONResponse);

			// getting the text to be rendered in the message
			const text = this.options.reduce((text, option) => {
				if (option.value == this.selected)
					text = option.text;
				return text;
			}, '');

			this.message = `Repositories filtered by ${text}:`;
			this.results = JSONResponse['response']['repositories'];

			// updating the number of requests remaining
			this.getRequestsRemainingVue();
		},
		getPopularReposVue : async function(event) {
			// setting flags to render only popular-repository component
			this.popularRepos = true;
			this.filteredRepos = !this.popularRepos;
			this.contributors = !this.popularRepos;

			this.message = 'Please wait while the server processes your request...';
			this.results = [];

			if (this.repoLanguage === '') {
				this.message = 'No language specified!';
				return;
			}

			const response = await fetch(
				`${APIRoot}/repos/popular/${encodeURIComponent(this.repoLanguage)}`, {
					cache : 'default',
				}
			);
			const JSONResponse = await response.json();
			// console.log(JSONResponse);

			if (JSONResponse['response'].hasOwnProperty('popular_repositories')) {
				this.message = `Popular repositories for ${this.repoLanguage}:`;
				this.results = JSONResponse['response']['popular_repositories'];

			} else {
				this.message = JSONResponse['response']['message'];
				this.results = [];
			}

			// updating the number of requests remaining
			this.getRequestsRemainingVue();
		},
		getTopContribsVue : async function(event) {
			// setting flags to render only contributor component
			this.contributors = true;
			this.filteredRepos = !this.contributors;
			this.popularRepos = !this.contributors;

			this.message = 'Please wait while the server processes your request...';
			this.results = [];

			if (this.repoURL === 'https://github.com/' || this.repoURL === '') {
				this.message = 'No repository URL specified!';
				return;
			}

			const response = await fetch(
				`${APIRoot}/repos/top-contribs/${this.repoURL}`, {
					cache : 'default',
				}
			);
			const JSONResponse = await response.json();
			// console.log(JSONResponse);

			if (JSONResponse['response'].hasOwnProperty('full_name')) {
				const repoName = JSONResponse['response']['full_name']

				this.message = `Top 5 Contributors for <a href="${this.repoURL}">${repoName}</a>:`;
				this.results = JSONResponse['response']['top_contributors'];

			} else {
				this.message = JSONResponse['response']['message'];
				this.results = [];
			}

			// updating the number of requests remaining
			this.getRequestsRemainingVue();
		}
	},
});

// event listeners for some nice interactivity
document.querySelector('#repo-url').addEventListener('focus', (event) => {
	app.repoURL = 'https://github.com/';
});
document.querySelector('#repo-url').addEventListener('blur', (event) => {
	if (app.repoURL == 'https://github.com/') {
		app.repoURL = '';
	}
});
