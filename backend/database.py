import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_PATH)

# print(load_dotenv(dotenv_path=".env", override=True))
DATABASE_URL = os.getenv("DATABASE_URL")

# def get_db():
#     return psycopg2.connect(
#         host="localhost",
#         database="manufacturing_core_db",
#         user="postgres",
#         password="admin#123",
#         cursor_factory=DictCursor
#     )




engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints SQL logs

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


