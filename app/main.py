from fastapi import FastAPI
from app.routers import url

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI(title="URL Shortener API")

# Creates limiter instance, using client IP as the identifier
limiter = Limiter(key_func=get_remote_address)

# Registers the limiter on the app state
app.state.limiter = limiter

# Registers handler that returns a proper 429 response when exceeds the allowed rate for client
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(url.router)