from typing import *

from pydantic import *


class InferenceSpeed(BaseModel):
    preprocess: float = 0.0
    inference: float = 0.0
    postprocess: float = 0.0


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class ClassificationProbability(BaseModel):
    pass


class DetectionBox(BaseModel):
    label: str = Field(alias="name")
    confidence: float = Field(alias="confidence")
    bbox: BoundingBox = Field(alias="box")


class OBBox(BaseModel):
    pass


class PoseKeypoint(BaseModel):
    pass


class SegmentMask(BaseModel):
    pass


class ClassificationResult(BaseModel):
    probs: List[ClassificationProbability]


class DetectionResult(BaseModel):
    boxes: List[DetectionBox]


class OBBResult(BaseModel):
    obbs: List[OBBox]


class PoseResult(BaseModel):
    keypoints: List[PoseKeypoint]


class SegmentResult(BaseModel):
    masks: List[SegmentMask]
