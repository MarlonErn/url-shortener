from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base

# --- MODEL URL ---
class URL(Base):
    # Table name used in DB
    __tablename__ = "urls"

    # Autoincrement
    __table_args__ = {"sqlite_autoincrement": True}

    # PK
    id = Column(Integer, primary_key=True, index=True)

    # SHORT_CODE
    # code to use in shortened url
    short_code = Column(String, unique=True, index=True, nullable=False)

    # ORIGINAL_URL
    # Long url to redirect navigation
    original_url = Column(String, nullable=False)

    # CREATED_AT
    # Date/Time creation
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # CLICKS
    # Access counter
    clicks = Column(Integer, default=0)