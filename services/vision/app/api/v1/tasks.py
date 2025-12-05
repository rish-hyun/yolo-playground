from fastapi import APIRouter, File, UploadFile

from models import (
    classification_model,
    detection_model,
    obb_model,
    pose_model,
    segmentation_model,
)
from schemas.responses import (
    ClassificationResponse,
    DetectionResponse,
    OBBResponse,
    PoseResponse,
    SegmentResponse,
)
from utils import img_bytes_to_cv2

router = APIRouter()


@router.post(
    "/classify",
    summary="Run classification on an image",
    response_model=ClassificationResponse,
)
async def classify_endpoint(file: UploadFile = File(...)):
    return {"message": "classify endpoint placeholder"}


@router.post(
    "/detect",
    summary="Run object detection on an image",
    response_model=DetectionResponse,
)
async def detect_endpoint(file: UploadFile = File(...)):
    # img_bytes = await file.read()
    # images = [img_bytes_to_cv2(img_bytes)]
    # result = detection_model(images)
    # return [res.to_json() for res in result]
    pass


@router.post(
    "/obb",
    summary="Run oriented bounding box detection on an image",
    response_model=OBBResponse,
)
async def obb_endpoint(file: UploadFile = File(...)):
    return {"message": "obb endpoint placeholder"}


@router.post(
    "/pose",
    summary="Run pose estimation on an image",
    response_model=PoseResponse,
)
async def pose_endpoint(file: UploadFile = File(...)):
    return {"message": "pose endpoint placeholder"}


@router.post(
    "/segment",
    summary="Run instance segmentation on an image",
    response_model=SegmentResponse,
)
async def segment_endpoint(file: UploadFile = File(...)):
    return {"message": "segment endpoint placeholder"}
