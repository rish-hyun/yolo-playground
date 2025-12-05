from typing import *

from pydantic import *


class InferenceSpeed(BaseModel):
    preprocessing: float
    inference: float
    postprocessing: float


class BoundingBox(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float


class ClassificationResult(BaseModel):
    pass


class DetectionResult(BaseModel):
    label: str
    confidence: float
    bbox: BoundingBox


class OBBResult(BaseModel):
    pass


class PoseResult(BaseModel):
    pass


class SegmentResult(BaseModel):
    pass
