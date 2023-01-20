from sqlalchemy import Column, String
from model import ModelBase


class Files(ModelBase):
    __tablename__ = 'files'
    path = Column(String(), primary_key=True)
    hash = Column(String(128), nullable=False)
