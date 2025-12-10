import mimetypes

import cv2
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from client import vision_client
from common.schemas.requests import ImageFile
from common.utils.convert import img_bytes_to_cv2, img_cv2_to_bytes_io


async def serialize(file: UploadFile = File(...)) -> ImageFile:
    if file.content_type.startswith("image/"):
        return ImageFile(
            file_name=file.filename,
            file_content=await file.read(),
            content_type=file.content_type,
        )
    elif file.content_type.startswith("video/"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Video files will be supported in future.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type.",
        )


router = APIRouter()


@router.post("/classify", summary="Run classification on an image")
async def classify(file: ImageFile = Depends(serialize)):
    pass


@router.post("/detect", summary="Run object detection on an image")
async def detect(file: ImageFile = Depends(serialize)):
    response = await vision_client.detect(file)
    img = img_bytes_to_cv2(file.file_content)

    result = response.results[0] or None
    for box in result.boxes:
        x1, y1, x2, y2 = (
            int(box.bbox.x1),
            int(box.bbox.y1),
            int(box.bbox.x2),
            int(box.bbox.y2),
        )
        label = f"{box.label} {box.confidence:.2f}"

        cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
        cv2.putText(
            img,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=2,
        )

    ext = mimetypes.guess_extension(file.content_type)
    img_bytes = img_cv2_to_bytes_io(img, ext=ext)

    return StreamingResponse(img_bytes, media_type=file.content_type)


@router.post("/obb", summary="Run oriented bounding box detection on an image")
async def obb(file: ImageFile = Depends(serialize)):
    pass


@router.post("/pose", summary="Run pose estimation on an image")
async def pose(file: ImageFile = Depends(serialize)):
    pass


@router.post("/segment", summary="Run segmentation on an image")
async def segment(file: ImageFile = Depends(serialize)):
    pass
