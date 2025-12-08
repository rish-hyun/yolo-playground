import os
import sys

_ROOT = os.path.join(os.path.dirname(__file__), "../../..")
if _ROOT not in sys.path and os.path.isdir(os.path.join(_ROOT, "common")):
    sys.path.insert(0, _ROOT)

from fastapi import FastAPI

from api.v1.tasks import router as orchestrator_router

app = FastAPI(
    title="Orchestrator Service",
    description="Coordinates requests between UI and Vision API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Orchestrator service is running"}


app.include_router(orchestrator_router, prefix="/api/v1", tags=["orchestrator"])
