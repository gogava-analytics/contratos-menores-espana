import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

# Engine SIN base de datos (solo para crearla)
_engine_server = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}"
)

with _engine_server.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db}"))
    conn.commit()

# Engine FINAL (este es el bueno)
engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"
)
