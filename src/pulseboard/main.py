from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from pulseboard.api.charts import router as charts_router
from pulseboard.api.points import router as points_router
from pulseboard.database import init_db

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
STATIC_DIR = WEB_DIR / "static"
TEMPLATES_DIR = WEB_DIR / "templates"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on application startup
    init_db()
    yield


app = FastAPI(title="Pulseboard API", version="0.1.0", lifespan=lifespan)

# Mount Static Files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Setup Jinja2 Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Include API Routers
app.include_router(charts_router, prefix="/api")
app.include_router(points_router, prefix="/api")


@app.get("/favicon.ico", include_in_schema=False)
async def serve_favicon():
    return FileResponse(STATIC_DIR / "favicon.ico")


@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse(request, "index.html")
