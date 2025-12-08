from typing import List

import numpy as np
from common.utils import img_bytes_to_cv2
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status


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


@router.post("/detect")
async def test(images: np.ndarray = Depends(serialize)):
    return {"message": "Test endpoint working"}
