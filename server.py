#!/usr/bin/env python3
from pydantic import BaseSettings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pathlib import Path

class ServerSettings(BaseSettings):
    hostname: str = '0.0.0.0'
    port: int = 9999

module_path = Path(__file__).parent.absolute()

app = FastAPI()
app.mount("/static", StaticFiles(directory=module_path / "static"), name="static")
templates = Jinja2Templates(directory=module_path / "templates")

def get_pics() -> list[str]:
    return glob.glob(str(module_path / 'static/*'), recursive=True)

@app.get("/")
def root(self, request: Request) -> HTMLResponse:
    """Return a response."""
    response = templates.TemplateResponse(
        'index.html',
        {'request': request, 'pics': get_pics()}
    )
    # The most important feature of this webserver
    response.init_headers({'x-clacks-overhead': 'long live Terry'})
    return response

def main(settings: ServerSettings | None=None):
    """Run webserver with default settings or the given settings."""
    if settings is None:
        settings = ServerSettings(
        # type: ignore
    )
    host = f'{settings.hostname}:{settings.port}'
    # app.start(host, name='sample_http')

if __name__ == '__main__':
    main()
