from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import URLCreate, URLResponse
from app.services.url_service import create_short_url, get_url_by_short_code


router = APIRouter()


@router.post("/shorten", response_model=URLResponse)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    new_url = create_short_url(db, str(payload.original_url))
    return new_url


@router.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    url_entry = get_url_by_short_code(db, short_code)

    if url_entry is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    url_entry.clicks += 1
    db.commit()

    return RedirectResponse(url=url_entry.original_url, status_code=302)


@router.get("/{short_code}/stats", response_model=URLResponse)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    url_entry = get_url_by_short_code(db, short_code)

    if url_entry is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return url_entry