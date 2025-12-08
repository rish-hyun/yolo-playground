from enum import StrEnum, auto

# from ultralytics.utils.downloads import GITHUB_ASSETS_NAMES


class ModelVersion(StrEnum):
    YOLO11N = auto()


class Task(StrEnum):
    DETECT = auto()
    SEGMENT = auto()
    CLASSIFY = auto()
    POSE = auto()
    OBB = auto()
