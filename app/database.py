from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


# the engine, the responsible part for connecting to the db
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# our session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# create a session to perform am SQL operation and then close it when completed.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
