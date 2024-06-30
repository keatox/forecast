# <img src='src/frontend/static/imgs/logo_small.png' width=200/>

Stock prediction [dashboard](https://forecastapp.onrender.com/) utilizing Monte Carlo to simulate Brownian Motion, and a Support Vector Machine to calculate public sentiment of stocks.

## Dependencies
Developed and tested using Python 3.12

Install necessary libraries using `pip install -r requirements`

## Quickstart

Create a .env file in root directory with the following variables initialized:

`REDDIT_API_KEY`,
`REDDIT_API_SECRET`,
`POSTGRES_PASSWORD`,
`POSTGRES_HOST`,
`POSTGRES_USER`,
`POSTGRES_PORT`,
`POSTGRES_DB`

If creating a new database, uncomment the code in the __init __ of database.py upon first deployment.

### Running locally

Navigate to `src/backend/app.py`

Comment out `app.run(debug=True,host='0.0.0.0')` and uncomment `app.run(debug=True)`

Run `app.py`

### Running on Docker
Navigate to root of project folder and run `docker compose up --build`

Your application will be available at http://localhost:5001

### Deploying to cloud

Build image using `docker build -t myapp . `  
(for macOS use `docker build --platform=linux/amd64 -t myapp .`)

Push to registry, e.g. `docker push myregistry.com/myapp`