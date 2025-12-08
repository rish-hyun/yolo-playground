from io import BytesIO

import cv2
import numpy as np


def img_bytes_to_cv2(img_bytes: bytes) -> np.ndarray:
    return cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)


def img_cv2_to_bytes_io(img: np.ndarray, ext: str) -> BytesIO:
    return BytesIO(cv2.imencode(ext, img)[1].tobytes())
