from pydantic import BaseModel, HttpUrl, ConfigDict
from datetime import datetime


# What must be sent in POST request
class URLCreate(BaseModel):
    original_url: HttpUrl


# Data returned by the API
class URLResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    short_code: str
    original_url: HttpUrl
    created_at: datetime
    clicks: int