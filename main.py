import hashlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="URL Shortener API")

# In-memory storage for shortened URLs
url_db: dict[str, str] = {}


class ShortenRequest(BaseModel):
    url: HttpUrl


class ShortenResponse(BaseModel):
    short_id: str
    original_url: str


@app.get("/")
def read_root():
    return {"message": "URL Shortener API is running"}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(request: ShortenRequest):
    url_str = str(request.url)
    short_id = hashlib.sha256(url_str.encode()).hexdigest()[:6]
    url_db[short_id] = url_str
    return ShortenResponse(short_id=short_id, original_url=url_str)


@app.get("/{short_id}")
def redirect_to_url(short_id: str):
    if short_id not in url_db:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=url_db[short_id], status_code=307)
