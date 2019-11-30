function get_repo_filter() {
	const filters = document.querySelector("#filter");
	const filter = filters.options[filters.selectedIndex].value;
	console.log(filter);
	return filter;
}

function get_repo_lang() {
	const lang = document.querySelector('#lang').value;
	console.log(lang)
	return lang;
}

function get_repo_url() {
	const repo_url = document.querySelector('#repo-url').value;
	console.log(repo_url);
	return repo_url;
}

async function get_filtered_repos() {
	const filter = get_repo_filter();
	const response = await fetch(
		`${window.origin}/api/repos/filter/${filter}`
	);
	const JSONResponse = await response.json();
	// console.log(JSONResponse);
	const results = JSONResponse['repositories'];
	for (let result of results) {
		console.log(result['full_name'], result['html_url'],
			result['stargazers_count'], result['contributors_count'],
			result['language']
		);
	}
}

async function get_popular_repos() {
	const lang = get_repo_lang();
	const response = await fetch(
		`${window.origin}/api/repos/${lang}`,
	);
	const JSONResponse = await response.json();
	// console.log(JSONResponse);
	const results	= JSONResponse['popular_repositories'];
	for (let result of results) {
		console.log(
			result['full_name'], result['html_url'],
			result['stargazers_count'], result['language']
		);
	}
}

async function get_top_contribs() {
	const repo_url = get_repo_url();
	const response = await fetch(
		`${window.origin}/api/repos/${repo_url}/top-contribs`,
	);
	const JSONResponse = await response.json();
	// console.log(JSONResponse);
	const results = JSONResponse['top_contributors'];
	for (let result of results) {
		console.log(result['html_url'], result['contributions']);
	}
}