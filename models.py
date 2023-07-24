from settings import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel


class Words(Base):
    __tablename__ = 'translator'
    id = Column(Integer, primary_key=True)
    eng = Column(String)
    ua = Column(String)


class UsersTable(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    points = Column(Integer)



class AddWord(BaseModel):
    ua: str
    eng: str


class EditWord(BaseModel):
    before_word: str
    after_word: str


class CreateUser(BaseModel):
    login: str
    password: str
