# TripMoksha-Task

Take Home Task given by TripMoksha for Backend Development internship.

## Overview

Make an app that utilizes the GitHub API and creates a wrapper library around it that has it's own custom end-points (REST API format).

## To Do

Utilize the GitHub API to create a wrapper REST-API that can return the following responses in JSON:

* Return the most popular repositories based on a filter like *open pull requests*, *number of commits* and *number of contributors*. Once filtered, the following 3 information **NEEDS** to be there:

    1. number of stars
    2. number of contributors, and
    3. primary programming language used by the repo

There should be an option to go to the GitHub link of the repo.

* Return popular repositories for different languages. Feel free to choose any 3 languages. The choice need **NOT** be configurable, just choose any 3 languages and implement based on your static choice.

* Return top 5 contributors for any repo.

## Bonus Task

* A front-end to test the REST-API which shows formatted JSON response in an easy-to-read format.
* Containerize the app using Docker.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Animesh-Ghosh/TripMoksha-Task.git
```

2. Create virtual environment:

```bash
python3 -m venv venv
```

3. Activate virtual environment:

	**Linux**
	```bash
	source venv/bin/activate
	```
	**Windows**
	```pwsh
	.\venv\Scripts\activate
	```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Add GitHub OAUTH TOKEN:
* Create a personal access token from [here](https://github.com/settings/tokens).
* Add the token in a `.env` file as `OAUTH_TOKEN='{YOUR_OAUTH_TOKEN}'`.

## Run

1. Run the development server:

```bash
flask run
```

2. Either go to [site](127.0.0.1:5000) being served by Flask server or use cURL or some other API client.

*Some notes:*
* Initially, server will be slow to start. However, after making the first requests, it will have cached the results.