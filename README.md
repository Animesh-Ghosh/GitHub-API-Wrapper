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