from lib.sqlachemy_imports import *
from config.flask_init import os

_db_dir = "../../data/sqlite/Assignment.db"
_SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(_db_dir)

ENGINE = create_engine(_SQLALCHEMY_DATABASE_URI, echo=True)

def create_session():
    Session = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
    return Session()




