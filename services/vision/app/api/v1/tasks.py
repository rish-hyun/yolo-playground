from typing import List

import numpy as np
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

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
from schemas.results import DetectionBox, DetectionResult, InferenceSpeed
from utils import img_bytes_to_cv2


async def serialize(file: UploadFile = File(...)) -> List[np.ndarray]:
    if file.content_type.startswith("image/"):
        return [img_bytes_to_cv2(await file.read())]
    elif file.content_type.startswith("video/"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Video files are not supported yet.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type.",
        )


router = APIRouter()


@router.post(
    "/classify",
    summary="Run classification on an image",
    response_model=ClassificationResponse,
)
async def classify_endpoint(images: np.ndarray = Depends(serialize)):
    # results = classification_model(images)
    return ClassificationResponse(results=[], speed=InferenceSpeed())


@router.post(
    "/detect",
    summary="Run object detection on an image",
    response_model=DetectionResponse,
)
async def detect_endpoint(images: np.ndarray = Depends(serialize)):
    results = []
    for res in detection_model(images):
        result = DetectionResult(boxes=[DetectionBox(**data) for data in res.summary()])
        results.append(result)
    return DetectionResponse(results=results, speed=InferenceSpeed(**res.speed))


@router.post(
    "/obb",
    summary="Run oriented bounding box detection on an image",
    response_model=OBBResponse,
)
async def obb_endpoint(images: np.ndarray = Depends(serialize)):
    # results = obb_model(images)
    return OBBResponse(results=[], speed=InferenceSpeed())


@router.post(
    "/pose",
    summary="Run pose estimation on an image",
    response_model=PoseResponse,
)
async def pose_endpoint(images: np.ndarray = Depends(serialize)):
    # results = pose_model(images)
    return PoseResponse(results=[], speed=InferenceSpeed())


@router.post(
    "/segment",
    summary="Run instance segmentation on an image",
    response_model=SegmentResponse,
)
async def segment_endpoint(images: np.ndarray = Depends(serialize)):
    # results = segmentation_model(images)
    return SegmentResponse(results=[], speed=InferenceSpeed())
