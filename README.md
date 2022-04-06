# Flash Card Study

View the App at https://shielded-basin-24478.herokuapp.com/

If there are no words in bin 0 and all other words still have positive timers, display a message: “You are temporarily done; please come back later to review more words.”

## Setup

### Run with Docker

Copy the `.env.SAMPLE` file and rename it `.env`.

Set your POSTGRES_USER and POSTGRES_PASSWORD variables (from docker-compose) in the `docker-compose.yml` file.

In the `.env` file, update the DATABASE_URI variable by adding the Username and Password.

Bring up the site with:
`docker-compose up`

## Database

To manage the database, run the docker-compose and enter the flask container:
`docker ps`
`docker exec -it CONTAINER_ID sh`

If you are doing a clean install, first run:
`flask db init`

If you need to make changes to the database (add or update db classes) then run:
`flask db migrate -m "Some message."`
`flask db upgrade`

To wipe the database, first take down the postgres container, then run:
`docker ps -a` - get the postgres container ID
`docker rm POSTGRES_CONTAINER_ID`
`docker volume ls` - get the pgdata volume name
`docker volume rm PGDATA_VOLUME_NAME`
Then clear the contents of the migrations folder.

## Development

Frontend
`cd src/ui`
`npm run dev`

Backend
`docker-compose up`

## Heroku

DEPLOY TO HEROKU
Once container and postgres addon are configured.
Update .env.PROD with heroku postgres URI
Run prod container locally
Run database commands above to initialize

Commands:

docker build -t registry.heroku.com/shielded-basin-24478/web -f ./deploy/docker/Dockerfile.prod .

docker push registry.heroku.com/shielded-basin-24478/web

heroku container:release --app shielded-basin-24478 web
