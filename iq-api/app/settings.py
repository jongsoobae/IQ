from starlette.config import Config

config = Config(".env")


DB_USER = config("MONGO_INITDB_ROOT_USERNAME")
DB_PASSWORD = config("MONGO_INITDB_ROOT_PASSWORD")
DB_HOST = config("MONGO_HOST")
DB_PORT = config("MONGO_PORT")


CORS_ALLOWED = config("CORS_ALLOWED").split(",")
