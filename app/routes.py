from fastapi import APIRouter, Request
from jinja2_fragments.fastapi import Jinja2Blocks

from app.config import settings
from app.repository.tinydb.CRUD import CRUD
from app.repository.artist import ArtistRepository


templates = Jinja2Blocks(directory=settings.TEMPLATE_DIR)
router = APIRouter()


@router.get("/")
def index(request: Request):
    with ArtistRepository() as repository:
        random_artist = repository.get_random_artist()
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "artist": random_artist,
            "page_title": "\N{Beamed Eighth Notes} Music Viewer",
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
    with ArtistRepository() as repository:
        artists = repository.get_all_artists()
    return templates.TemplateResponse(
        "catalog.html",
        {
            "request": request,
            "artists": artists,
        }
    )

@router.get("/artist/{artist_id}")
def artist(request: Request, artist_id: int):
    with ArtistRepository() as repository:
        artist = repository.get_artist(id=artist_id)
    return templates.TemplateResponse(
        "artist.html",
        {
            "request": request,
            "artist": artist,
        }
    )