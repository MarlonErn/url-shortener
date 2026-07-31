from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import URLCreate, URLResponse
from app.services.url_service import create_short_url, get_url_by_short_code, get_url_by_original_url

from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter()

# Same key function (client IP) used by the main limiter in main.py
limiter = Limiter(key_func=get_remote_address)

@router.post("/shorten", response_model=URLResponse)
@limiter.limit("10/minute")
def shorten_url(request: Request, payload: URLCreate, response: Response, db: Session = Depends(get_db)):
    check_url = get_url_by_original_url(db, str(payload.original_url))

    if check_url:
        response.status_code = 200
        return check_url
    else:
        new_url = create_short_url(db, str(payload.original_url))
        response.status_code = 201
        return new_url


@router.get("/{short_code}")
@limiter.limit("60/minute")
def redirect_to_original(request: Request, short_code: str, db: Session = Depends(get_db)):
    url_entry = get_url_by_short_code(db, short_code)

    if url_entry is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    url_entry.clicks += 1
    db.commit()

    return RedirectResponse(url=url_entry.original_url, status_code=302)


@router.get("/{short_code}/stats", response_model=URLResponse)
@limiter.limit("60/minute")
def get_url_stats(request: Request, short_code: str, db: Session = Depends(get_db)):
    url_entry = get_url_by_short_code(db, short_code)

    if url_entry is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return url_entry