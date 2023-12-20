# Importing necessary modules and setting up the database connection.
from lib.sqlachemy_imports import *
from config.flask_init import os

_db_dir = "data/sqlite/Assignment.db"
_SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(_db_dir)

ENGINE = create_engine(_SQLALCHEMY_DATABASE_URI, echo=True)


def create_session():
    """
    The function creates and returns a session object for database operations.

    :return: an instance of the Session class.
    """
    Session = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
    return Session()
