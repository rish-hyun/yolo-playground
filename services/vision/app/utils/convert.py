import cv2
import numpy as np


def img_bytes_to_cv2(img_bytes: bytes):
    return cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
