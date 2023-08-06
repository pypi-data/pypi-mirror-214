import os
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
)
from sqlalchemy.engine import create_engine
from dotenv import load_dotenv
from constants.env import (
    DATABASE_URI_ENV_VARIABLE_KEY,
    DATABASE_URI_DEFAULT,
)


load_dotenv()
Base = declarative_base()


engine = create_engine(os.getenv(DATABASE_URI_ENV_VARIABLE_KEY, DATABASE_URI_DEFAULT))
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    try:
        Base.metadata.create_all(engine)
        session = LocalSession()
        yield session
    finally:
        session.close()
