# app/api/v1/tasks.py

import cv2
import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile
from models import detect_model  # your DetectModel instance
from starlette.status import HTTP_400_BAD_REQUEST

# TODO: Add imports for other models when available
# from models import segment_model, classify_model, pose_model, obb_model


def imgbytes_to_cv2(img_bytes: bytes):
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # BGR
    return img


router = APIRouter()


def validate_image(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}",
        )


@router.post("/detect", summary="Run object detection on an image")
async def detect_endpoint(file: UploadFile = File(...)):
    validate_image(file)
    img_bytes = await file.read()
    try:
        result = detect_model(images=[imgbytes_to_cv2(img_bytes)])
        return [res.to_json() for res in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/segment", summary="Run instance segmentation on an image")
async def segment_endpoint(file: UploadFile = File(...)):
    validate_image(file)
    # TODO: Call segment_model.predict(img_bytes)
    return {"message": "segment endpoint placeholder"}


@router.post("/classify", summary="Run classification on an image")
async def classify_endpoint(file: UploadFile = File(...)):
    validate_image(file)
    # TODO: Call classify_model.predict(img_bytes)
    return {"message": "classify endpoint placeholder"}


@router.post("/pose", summary="Run pose estimation on an image")
async def pose_endpoint(file: UploadFile = File(...)):
    validate_image(file)
    # TODO: Call pose_model.predict(img_bytes)
    return {"message": "pose endpoint placeholder"}


@router.post("/obb", summary="Run oriented bounding box detection on an image")
async def obb_endpoint(file: UploadFile = File(...)):
    validate_image(file)
    # TODO: Call obb_model.predict(img_bytes)
    return {"message": "obb endpoint placeholder"}
