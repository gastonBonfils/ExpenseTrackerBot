# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///expenses.db")  # real file, not memory
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Create all tables if they don't exist yet."""
    Base.metadata.create_all(engine)
