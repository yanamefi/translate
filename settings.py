import sqlite3
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()


engine = create_engine('postgresql://docker:postgresql@localhost:5432/translator')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()