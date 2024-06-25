# Forecast

## Quickstart:
create .env in root with REDDIT_API_SECRET, REDDIT_API_KEY, POSTGRES_PASSWORD, POSTGRES_HOST = localhost

### To run locally

navigate to src/backend/app.py

comment out app.run(debug=True,host='0.0.0.0') and uncomment app.run(debug=True)

run code

### To run on Docker
navigate to root of project folder and run

`docker compose up --build`.

Your application will be available at http://localhost:5001.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.