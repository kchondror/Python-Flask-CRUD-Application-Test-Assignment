from sqlalchemy import create_engine, Column, Integer, String, CHAR
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from contextlib import contextmanager