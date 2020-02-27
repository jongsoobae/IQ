from starlette.config import Config

config_docker = Config("../docker/.env")


DB_USER = config_docker("MONGO_ROOT_USER")
DB_PASSWORD = config_docker("MONGO_ROOT_USER")
DB_HOST = "127.0.0.1"
DB_PORT = config_docker("MONGO_PORT")


CORS_ALLOWED = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]
