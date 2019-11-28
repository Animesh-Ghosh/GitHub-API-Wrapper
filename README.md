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
