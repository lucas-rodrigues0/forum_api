from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from sqlalchemy_utils import database_exists, create_database
from os import environ as env
from dotenv import find_dotenv, load_dotenv


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

config = {
    "dbname": env.get("PG_DATABASE"),
    "user": env.get("PG_USER"),
    "password": env.get("PG_PASSWORD"),
    "host": env.get("PG_HOST"),
    "port": env.get("PG_PORT"),
}

# # cria a engine de conexão com o banco
# dialect+driver://username:password@host:port/database
postgres_url = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"

engine = create_engine(postgres_url)

# cria o database caso não exista
if not database_exists(engine.url):
    create_database(engine.url)

inspector = inspect(engine)


# Instancia um criador de seção com o banco
db_session = sessionmaker(bind=engine)
