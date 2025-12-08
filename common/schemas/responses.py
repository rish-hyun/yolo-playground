from typing import Generic, List, TypeVar

from pydantic import BaseModel

from .results import (
    ClassificationResult,
    DetectionResult,
    InferenceSpeed,
    OBBResult,
    PoseResult,
    SegmentResult,
)

T = TypeVar("T")


class ModelResponse(BaseModel, Generic[T]):
    results: List[T]
    speed: InferenceSpeed


ClassificationResponse = ModelResponse[ClassificationResult]
DetectionResponse = ModelResponse[DetectionResult]
OBBResponse = ModelResponse[OBBResult]
PoseResponse = ModelResponse[PoseResult]
SegmentResponse = ModelResponse[SegmentResult]
