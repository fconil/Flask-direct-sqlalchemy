from sqlalchemy import Column, Integer, String

from mymodels.base import MyBase


class Author(MyBase):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
