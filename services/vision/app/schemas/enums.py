from enum import StrEnum, auto


class ModelVersion(StrEnum):
    YOLO11N = auto()


class Task(StrEnum):
    DETECT = auto()
    SEGMENT = auto()
    CLASSIFY = auto()
    POSE = auto()
    OBB = auto()
