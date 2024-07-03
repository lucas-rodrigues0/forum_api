from os import environ as env
from dotenv import find_dotenv, load_dotenv

from api import api
from graphql_api.db import inspector, recreate_database


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


if __name__ == "__main__":
    if not inspector.get_table_names():
        recreate_database()

    api.run(
        host="0.0.0.0", port=env.get("API_PORT", 4444), debug=env.get("DEBUG", False)
    )
