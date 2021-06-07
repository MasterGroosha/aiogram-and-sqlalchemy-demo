# aiogram-and-sqlalchemy-demo
A simple demo of using aiogram + async sqlalchemy 1.4+

Used tech:
* [aiogram](https://github.com/aiogram/aiogram)
* [SQLAlchemy 1.4+](https://www.sqlalchemy.org/)
* PostgreSQL as database
* asyncpg as database driver for SQLAlchemy
* Docker with docker-compose for deployment

Don't forget to create "postgres_data" (required) and "pgadmin_data" (if using PG Admin) directories 
before you run `docker-compose up -d`

Also copy `env_dist` file to `.env` and fill it with your data
