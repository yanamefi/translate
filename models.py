from settings import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel


class Words(Base):
    __tablename__ = 'translator'
    id = Column(Integer, primary_key=True)
    eng = Column(String)
    ua = Column(String)


class AddWord(BaseModel):
    ua: str
    eng: str


class EditWord(BaseModel):
    before_word: str
    after_word: str

