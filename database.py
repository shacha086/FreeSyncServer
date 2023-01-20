import config
from model import *
from pathlib import Path
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

engine = create_engine(f"sqlite:///{(Path(config.db_path) / config.db_name).absolute()}")
if not database_exists(engine.url):
    create_database(engine.url)

ModelBase.metadata.create_all(engine)
Session: sessionmaker = sessionmaker(bind=engine)
