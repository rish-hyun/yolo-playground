from schemas.enums import ModelVersion

from .classify import ClassificationModel
from .detect import DetectionModel
from .obb import OBBModel
from .pose import PoseModel
from .segment import SegmentationModel

model_version = ModelVersion.YOLO11N

classification_model = ClassificationModel(model_version)
detection_model = DetectionModel(model_version)
obb_model = OBBModel(model_version)
pose_model = PoseModel(model_version)
segmentation_model = SegmentationModel(model_version)
