from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.crud import CRUD


templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)
router = APIRouter()


@router.get("/")
def index(request: Request):
    db = CRUD.with_table("artist_info")
    random_artist = db.get_random_item()
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "artist": random_artist,
        }
    )


@router.get("/hello")
def hello(request: Request):
    return templates.TemplateResponse(
        "shared/_base.html", 
        {
            "request": request,
            "page_title": "\N{Waving Hand Sign} Hello there!",
        }
        )


@router.get("/main")
def main(request: Request):
    return templates.TemplateResponse(
        "main.html", 
        {
            "request": request,
            "page_description": "Main page for pyHAT (python, htmx, awsgi, tailwind)",
            "page_title": "Main page",
        }
        )


@router.get("/catalog")
def catalog(request: Request):
    db = CRUD.with_table("artist_details")
    artists = db.all_items()
    return templates.TemplateResponse(
        "catalog.html",
        {
            "request": request,
            "artists": artists,
        }
    )

@router.get("/artist/{artist_id}")
def artist(request: Request, artist_id: int):
    db = CRUD.with_table("artist_info")
    artist = db.find(key="id", value=artist_id)[0]
    db = CRUD.with_table("artist_details")
    artist_details = db.find(key="id", value=artist_id)[0]
    return templates.TemplateResponse(
        "artist.html",
        {
            "request": request,
            "artist": artist,
            "details": artist_details,
        }
    )