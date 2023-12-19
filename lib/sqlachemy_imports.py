# Importing various modules and classes from the SQLAlchemy library
from sqlalchemy import create_engine, Column, Integer, String, VARCHAR
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.sql import text
from contextlib import contextmanager
