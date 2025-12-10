from io import BytesIO

import cv2
import numpy as np


def img_bytes_to_cv2(img_bytes: bytes) -> np.ndarray:
    return cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)


def img_cv2_to_bytes_io(img: np.ndarray, ext: str) -> BytesIO:
    return BytesIO(cv2.imencode(ext, img)[1].tobytes())


def hex_to_rgb(hex: str) -> tuple[int, int, int]:
    return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2]).upper()
