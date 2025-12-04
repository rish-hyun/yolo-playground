from schemas.enums import ModelVersion

from .detect import DetectModel

detect_model = DetectModel(model_version=ModelVersion.YOLO11N)
