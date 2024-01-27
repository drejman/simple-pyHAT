from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.config import settings


templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)
router = APIRouter()


@router.get("/")
def index():
    return """
        <html>
            <head>
                <title>Simple Site</title>
            </head>
            <body>
                <h1>Hello World!</h1>
            </body>
        </html>
        """


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
