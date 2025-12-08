import mimetypes

from common.schemas.requests import ImageFile
from common.utils import img_bytes_to_cv2, img_cv2_to_bytes_io
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from client import vision_client


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
