from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus as urlquote
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL % urlquote(settings.database_password))

SessionLocal = sessionmaker(
    autocommit=False , autoflush=False , bind=engine
)

Base = declarative_base()

"""Dependency"""
def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""Database Connection"""
def connectToDB():
    while True:
        try:
            """Connect to your postgres DB"""
            conn = psycopg2.connect(host='localhost' , database='postgres' , user='postgres' , password='@hitesh22' , cursor_factory=RealDictCursor)

            """Open a cursor to perform database operations"""
            conn.cursor()
            print('Databse connection was successfull!')
            break

        except Exception as error:
            print('Connecting to Database failed')
            print('Error : ',error)
            time.sleep(2)