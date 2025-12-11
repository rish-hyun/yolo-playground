import os

from common.schemas.enums import ModelVersion

from .models import (
    ClassificationModel,
    DetectionModel,
    OBBModel,
    PoseModel,
    SegmentationModel,
)

model_version = ModelVersion(os.getenv("MODEL_VERSION", ModelVersion.YOLO11N.value))

classification_model = ClassificationModel(model_version)
detection_model = DetectionModel(model_version)
obb_model = OBBModel(model_version)
pose_model = PoseModel(model_version)
segmentation_model = SegmentationModel(model_version)
