from fastapi import FastAPI

from api.v1.tasks import router as vision_router

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


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Vision service is running"}


app.include_router(vision_router, prefix="/api/v1", tags=["vision"])
