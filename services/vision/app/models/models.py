from common.schemas.enums import Task

from .base import BaseYOLOModel


class ClassificationModel(BaseYOLOModel):
    task: Task = Task.CLASSIFY


class DetectionModel(BaseYOLOModel):
    task = Task.DETECT


class OBBModel(BaseYOLOModel):
    task: Task = Task.OBB


class PoseModel(BaseYOLOModel):
    task: Task = Task.POSE


class SegmentationModel(BaseYOLOModel):
    task: Task = Task.SEGMENT
