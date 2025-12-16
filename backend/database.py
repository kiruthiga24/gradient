import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

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


