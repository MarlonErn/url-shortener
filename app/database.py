from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -- URL CONNECTION --
DATABASE_URL = "sqlite:///./url_shortener.db"

# -- ENGINE --
# "check_same_thread" parameter required for SQLite (requests across different threads are not required in this project).
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# -- SESSIONLOCAL -- 
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -- DECLARATIVE BASE --
Base = declarative_base()

# -- DEPENDENCY get_db() --
# close every single session used, and close the connection.
# try/finally used to close session even when gets error
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()