from enum import StrEnum, auto


class ModelVersion(StrEnum):
    YOLO11N = auto()
    YOLO11S = auto()
    YOLO11M = auto()
    YOLO11L = auto()
    YOLO11X = auto()


class Task(StrEnum):
    DETECT = auto()
    SEGMENT = auto()
    CLASSIFY = auto()
    POSE = auto()
    OBB = auto()
