import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base


@pytest.fixture
def db_session():
    """
    Creates a fresh in-memory SQLite database for each test that
    requests this fixture, builds the schema from the models,
    yields a session for the test to use, and cleans up afterwards.
    """

    # DB for testing. Only exists in RAM.
    engine = create_engine("sqlite:///:memory:")

    # Create tables. Needs previous importation from models
    Base.metadata.create_all(bind=engine)

    # Creates session w/ test engine
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()

    yield session

    session.close()