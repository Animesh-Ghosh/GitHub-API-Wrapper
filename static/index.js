// not a JS user, only used what I could find useful

// helper function to get the filter
function get_repo_filter() {
  const filters = document.querySelector("#filter");
  const filter = filters.options[filters.selectedIndex].value;
  return filter;
}

// helper function to get the language
function get_repo_lang() {
  const lang = document.querySelector('#lang').value;
  return lang;
}

// helper function to get the URL
function get_repo_url() {
  const repo_url = document.querySelector('#repo-url').value;
  return repo_url;
}

// helper function to set message
function set_message(message) {
  document.querySelector('#message').innerHTML = message;
}

// fetches the repositories and shows results
async function get_filtered_repos() {
  set_message('Please wait while the server processes your request...');

  // getting filter
  const filter = get_repo_filter();
  const response = await fetch(
    `${window.origin}/api/repos/filter/${filter}`
  );
  const JSONResponse = await response.json();
  const results = JSONResponse['repositories'];

  // rendering results
  let filter_message = null;
  switch (filter) {
    case 'prs':
      filter_message = 'Open Pull Requests';
      break;
    case 'commits':
      filter_message = 'Number of Commits';
      break;
    case 'contribs':
      filter_message = 'Number of Contributors';
      break;
  }
  const message = `Repositories sorted by ${filter_message}:`;
  set_message(message);

  const ol = document.querySelector('#result');
  ol.innerHTML = '';
  for (result of results) {
    let li = document.createElement('li');
    let span = document.createElement('span');
    span.innerHTML = `
      <a href="${result['html_url']}">${result['full_name']}</a><br/>
      Stars: ${result['stargazers_count']}<br/>
      Contributors: ${result['contributors_count']}<br/>
      Open Pull Requests: ${result['open_pull_requests_count']}<br/>
      Commits: ${result['commits_count']}<br/>
      Contributors: ${result['contributors_count']}
    `;
    li.appendChild(span);
    ol.appendChild(li);
  }
}

// fetches the repositories and shows results
async function get_popular_repos() {
  set_message('Please wait while the server processes your request...');

  // getting repo lang
  const lang = get_repo_lang();

  // fetching data
  const response = await fetch(
    `${window.origin}/api/repos/${lang}`,
  );
  const JSONResponse = await response.json();
  const results = JSONResponse['popular_repositories'];

  // rendering results
  const message = `Popular repositories for ${lang.toLowerCase()}:`;
  set_message(message);

  const ol = document.querySelector('#result');
  ol.innerHTML = '';
  for (result of results) {
    let li = document.createElement('li');
    let span = document.createElement('span');
    span.innerHTML = `
      <a href="${result['html_url']}">${result['full_name']}</a><br/>
      Stars: ${result['stargazers_count']}
    `;
    li.appendChild(span);
    ol.appendChild(li);
  }
}

// fetches the contributors and shows results
async function get_top_contribs() {
  set_message('Please wait while the server processes your request...');
  
  // getting repo URL
  const repo_url = get_repo_url();

  // fetching data
  const response = await fetch(
    `${window.origin}/api/repos/${repo_url}/top-contribs`,
  );
  const JSONResponse = await response.json();
  const results = JSONResponse['top_contributors'];

  // rendering results
  const repo_name = repo_url.split('https://github.com/')[1];
  const message = `Top 5 Contributors for <a href="${repo_url}">${repo_name}</a>:`;
  set_message(message);

  const ol = document.querySelector('#result');
  ol.innerHTML = '';
  for (result of results) {
    let li = document.createElement('li');
    let span = document.createElement('span');
    span.innerHTML = `
      <a href="${result['html_url']}">${result['login']}</a><br/>
      Contributions: ${result['contributions']}
    `;
    li.appendChild(span);
    ol.appendChild(li);
  }
}