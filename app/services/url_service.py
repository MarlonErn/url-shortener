import uuid

from sqlalchemy.orm import Session

from app.models import URL
from app.services.base62 import encode


def create_short_url(db: Session, original_url: str):
    # Set temporary short_code (not nullable field at DB)
    new_url = URL(
        original_url=original_url,
        short_code=f"__pending__{uuid.uuid4().hex}"
    )

    # Add url to the table and persist
    # Set id to generate short_code
    db.add(new_url)
    db.commit()

    # Refresh object w/ DB generated values (id, created_at)
    db.refresh(new_url)

    new_url.short_code = encode(new_url.id)

    # Update short_code at DB and persist
    db.commit()
    db.refresh(new_url)

    return new_url


def get_url_by_short_code(db: Session, short_code: str) -> URL | None:
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()

    return url_entry