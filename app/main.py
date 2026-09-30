from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="VS Code Server + JFrog POC")
APP_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
templates = Jinja2Templates(directory=APP_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={},
    )


@app.get("/display", response_class=HTMLResponse)
@app.get("/display.html", response_class=HTMLResponse, include_in_schema=False)
def display(request: Request, name: str = Query(default="", max_length=100)):
    name = name.strip()
    if name:
        print(f"Received name: {name}", flush=True)
    return templates.TemplateResponse(
        request=request,
        name="display.html",
        context={"name": name},
    )


@app.get("/health")
def health():
    return {"status": "UP"}
