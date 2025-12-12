import os
import sys

_ROOT = os.path.join(os.path.dirname(__file__), "../../..")
if _ROOT not in sys.path and os.path.isdir(os.path.join(_ROOT, "common")):
    sys.path.insert(0, _ROOT)

from fastapi import FastAPI

from api.v1.tasks import router as vision_router
from common.schemas.responses import HealthStatus

app = FastAPI(
    title="Vision Service",
    description=(
        "Unified service hosting multiple YOLO-based vision tasks:\n"
        "- Object Detection\n"
        "- Instance Segmentation\n"
        "- Classification\n"
        "- Pose Estimation\n"
        "- Oriented Bounding Boxes (OBB)"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get(
    "/health",
    tags=["system"],
    summary="Get vision service health status",
    response_model=HealthStatus,
)
async def health() -> HealthStatus:
    return HealthStatus(healthy=True, message="Vision service is running")


@app.get("/", include_in_schema=False, response_model=HealthStatus)
async def root() -> HealthStatus:
    return HealthStatus(healthy=True, message="Vision service is running")


app.include_router(vision_router, prefix="/api/v1", tags=["vision"])
